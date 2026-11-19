"""Versioned prompt contracts; no inputs are executed or assigned expectations."""

import base64
from dataclasses import dataclass
from importlib import resources
import json
import math
from string import Template
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


def strict_json(text):
    def constant(value):
        raise ValueError('non-finite JSON numbers are forbidden')
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(text, parse_constant=constant, object_pairs_hook=pairs)


def validate_input(value, depth=0):
    if depth > 30:
        raise ValueError('input nesting exceeds 30')
    if isinstance(value, dict):
        if '$bytes' in value:
            if set(value) != {'$bytes'} or not isinstance(value['$bytes'], str):
                raise ValueError('byte input must contain only a base64 $bytes field')
            base64.b64decode(value['$bytes'], validate=True)
        else:
            for item in value.values():
                validate_input(item, depth + 1)
    elif isinstance(value, list):
        for item in value:
            validate_input(item, depth + 1)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError('non-finite JSON numbers are forbidden')


class ProposedInput(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    category: Literal['typical', 'edge', 'empty', 'boundary', 'unicode', 'bytes']
    args_json: str = Field(max_length=16000)
    kwargs_json: str = Field(max_length=16000)
    reason: str = Field(min_length=1, max_length=800)

    @field_validator('args_json', 'kwargs_json')
    @classmethod
    def valid_arguments(cls, text, info):
        value = strict_json(text)
        expected = list if info.field_name == 'args_json' else dict
        if type(value) is not expected:
            raise ValueError('args_json must be an array; kwargs_json must be an object')
        for item in value if expected is list else value.values():
            validate_input(item)
        return text


class InputProposals(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    cases: list[ProposedInput] = Field(min_length=1, max_length=32)


class CharacterizationInput(ProposedInput):
    setup_json: str = Field(default='[]', max_length=16000)
    files_json: str = Field(default='{}', max_length=16000)

    @field_validator('setup_json', 'files_json')
    @classmethod
    def valid_setup(cls, text, info):
        value = strict_json(text)
        if info.field_name == 'files_json':
            if not isinstance(value, dict):
                raise ValueError('files_json must map scratch-relative paths to base64')
            for path, raw in value.items():
                if not path or path.startswith('/') or any(p in ('', '.', '..') for p in path.split('/')):
                    raise ValueError('unsafe scratch path')
                base64.b64decode(raw, validate=True)
        else:
            if not isinstance(value, list) or len(value) > 16:
                raise ValueError('setup_json must be at most 16 method calls')
            for call in value:
                if not isinstance(call, dict) or set(call) != {'method', 'args', 'kwargs'} or \
                        not isinstance(call['method'], str) or not call['method'].isidentifier() or \
                        call['method'].startswith('_') or not isinstance(call['args'], list) or \
                        not isinstance(call['kwargs'], dict):
                    raise ValueError('invalid setup method call')
                validate_input(call)
        return text


class CharacterizationInputs(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    cases: list[CharacterizationInput] = Field(min_length=1, max_length=32)


PROMPTS = {'input_proposals.v1': InputProposals,
           'characterization_inputs.v1': CharacterizationInputs}


@dataclass(frozen=True)
class Prompt:
    name: str
    text: str
    schema: dict
    response_model: type[BaseModel]

    def render(self, context):
        return Template(self.text).substitute(
            context=json.dumps(context, sort_keys=True, ensure_ascii=True, allow_nan=False),
            schema=json.dumps(self.schema, sort_keys=True))


def load_prompt(name):
    if name not in PROMPTS:
        raise ValueError('unknown prompt version: ' + name)
    directory = resources.files('modernize').joinpath('prompts')
    schema = strict_json(directory.joinpath(name + '.schema.json').read_text())
    model = PROMPTS[name]
    if schema != model.model_json_schema():
        raise ValueError('prompt schema differs from registered response model')
    return Prompt(name, directory.joinpath(name + '.txt').read_text(), schema, model)

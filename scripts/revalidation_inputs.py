"""Retain exposed cases as regressions; seal only fresh input-only candidates."""

import json
from pathlib import Path

from characterize_corpus import RecordedProposalClient, SEEDS
from modernize.characterize import digest
from modernize.llm import LLMResponse, TokenUsage
from modernize.llm_prompts import CharacterizationInput

FRESH = Path(__file__).resolve().parents[1] / 'tests/fixtures/cp11/revalidation_inputs.v2.json'


def exposed_ids(project):
    ids = set()
    for key, rounds in json.loads(SEEDS.read_text()).items():
        path, target = key.split('::')
        if not path.startswith(project + '/'):
            continue
        path = path[len(project) + 1:]
        for proposals in rounds:
            for proposal in proposals:
                case = dict(path=path, target=target, **CharacterizationInput.model_validate(proposal, strict=True).model_dump())
                identity = {k:v for k,v in case.items() if k not in ('category', 'reason')}
                ids.add(digest(json.dumps(identity, sort_keys=True).encode())[:20])
    return ids


class RevalidationProposalClient(RecordedProposalClient):
    def complete(self, prompt, **kwargs):
        response = super().complete(prompt, **kwargs)
        context = json.loads(prompt.split('Context JSON:\n', 1)[1])
        fn = context['function']
        key = context['project'] + '/' + fn['path'] + '::' + fn['target']
        cases = json.loads(response.text)['cases'] + json.loads(FRESH.read_text())[key]
        return LLMResponse(json.dumps(dict(cases=cases)), self.model, TokenUsage())

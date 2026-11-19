"""Strict, dependency-free configuration for the CP0 foundation."""

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path


@dataclass(frozen=True)
class Config:
    legacy_image: str = "modernize-legacy:cp0"
    modern_image: str = "modernize-modern:cp0"
    log_level: str = "INFO"

    def __post_init__(self):
        for name in ("legacy_image", "modern_image"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value or any(c.isspace() for c in value):
                raise ValueError(f"{name} must be a nonempty image reference without whitespace")
        if self.log_level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            raise ValueError("log_level must be DEBUG, INFO, WARNING, ERROR, or CRITICAL")

    def to_dict(self):
        return asdict(self)


def load_config(path: Path | None = None) -> Config:
    if path is None:
        return Config()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("configuration must be a JSON object")
    unknown = data.keys() - {field.name for field in fields(Config)}
    if unknown:
        raise ValueError("unknown configuration keys: " + ", ".join(sorted(unknown)))
    return Config(**data)

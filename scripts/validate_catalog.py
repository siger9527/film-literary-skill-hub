#!/usr/bin/env python3
"""Validate generated catalog records against the committed resource-card schema."""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def validate_catalog(path):
    schema = json.loads((ROOT / "schemas" / "resource-card.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    resources = payload.get("resources")
    if not isinstance(resources, list):
        raise ValueError("catalog payload must contain a resources array")
    errors = []
    for index, record in enumerate(resources):
        for error in validator.iter_errors(record):
            errors.append(f"resources[{index}] {".".join(map(str, error.absolute_path))}: {error.message}")
    if errors:
        raise ValueError("\n".join(errors))
    return len(resources)

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "catalog" / "generated" / "resources.json"
    print(f"Validated {validate_catalog(target)} resource cards against resource-card.schema.json")

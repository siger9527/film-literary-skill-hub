#!/usr/bin/env python3
"""Validate generated discovery and L1 review artifacts against committed schemas."""
import argparse
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def validate(path, schema_path, collection_key, count_key):
    schema = json.loads((ROOT / schema_path).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    records = payload.get(collection_key)
    if not isinstance(records, list):
        raise ValueError(f"artifact must contain a {collection_key} array")
    errors = []
    for index, record in enumerate(records):
        for error in validator.iter_errors(record):
            location = ".".join(map(str, error.absolute_path))
            errors.append(f"{collection_key}[{index}] {location}: {error.message}")
    if errors:
        raise ValueError("\n".join(errors))
    if count_key in payload and payload[count_key] != len(records):
        raise ValueError(f"{count_key} does not match {collection_key} length")
    return len(records)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=["resources", "l1", "l2"])
    parser.add_argument("--input")
    args = parser.parse_args()
    if args.kind == "resources":
        path = args.input or str(ROOT / "catalog" / "generated" / "resources.json")
        count = validate(path, "schemas/resource-card.schema.json", "resources", "count")
        print(f"Validated {count} resource cards.")
    elif args.kind == "l1":
        path = args.input or str(ROOT / "catalog" / "generated" / "l1-reviews.json")
        count = validate(path, "schemas/l1-review.schema.json", "reviews", "count")
        print(f"Validated {count} L1 review records.")
    else:
        path = args.input or str(ROOT / "catalog" / "generated" / "l2-reviews.json")
        count = validate(path, "schemas/l2-review.schema.json", "reviews", "count")
        print(f"Validated {count} L2 review records.")

#!/usr/bin/env python3
"""Validate the canonical V0.1 five-stage / 21-node taxonomy and board completeness."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / "config/categories.json").read_text(encoding="utf-8"))
index = json.loads((ROOT / "catalog/film-production-21-node-index.json").read_text(encoding="utf-8"))
expected = {f"{n:02d}" for n in range(21)}
indexed = {item["id"] for item in index["nodes"]}
category_nodes = [node for category in config["categories"] for node in category["nodes"]]
if config.get("schema_version") != "1.1.0":
    raise SystemExit("Unexpected taxonomy schema version")
if indexed != expected:
    raise SystemExit(f"Node index mismatch: missing={sorted(expected-indexed)}, extra={sorted(indexed-expected)}")
if len(index["nodes"]) != 21 or len(category_nodes) != 21 or set(category_nodes) != expected:
    raise SystemExit("Categories must map exactly one primary category to each of the 21 nodes")
if len(category_nodes) != len(set(category_nodes)):
    raise SystemExit("A node is duplicated across primary categories")
stage_nodes = [node for stage in config["stages"] for node in stage["nodes"]]
if set(stage_nodes) != expected or len(stage_nodes) != 21:
    raise SystemExit("Five stages must cover each node exactly once")
if config["stages"] != index["stages"]:
    raise SystemExit("Stage definitions differ between category config and node index")
if any(domain["id"] in {category["id"] for category in config["categories"]} for domain in config["cross_cutting_domains"]):
    raise SystemExit("Cross-cutting domains must not be primary production categories")
for domain in config["cross_cutting_domains"]:
    if not set(domain["maps_to_nodes"]) <= expected:
        raise SystemExit(f"Invalid node mapping in cross-cutting domain: {domain['id']}")
for node in index["nodes"]:
    if not (ROOT / "library" / "21-nodes" / f"{node['id']}-" ).exists():
        matches = list((ROOT / "library/21-nodes").glob(f"{node['id']}-*/README.md"))
        if len(matches) != 1:
            raise SystemExit(f"Missing or duplicate knowledge board for node {node['id']}")
print("PASS: 5 stages, 21 unique nodes, 21 primary categories, cross-cutting domains, and 21 board files.")

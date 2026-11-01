#!/usr/bin/env python3
"""Strictly validate the canonical five-stage / 21-node taxonomy and board integrity."""
import json
import re
import sys
from pathlib import Path

EXPECTED_STAGES = [
    ("stage-01", "项目立项与前期开发", ["00", "01", "02"]),
    ("stage-02", "导演与视觉前期", ["03", "04", "05", "06", "07", "08", "09"]),
    ("stage-03", "资产与镜头制作", ["10", "11", "12", "13"]),
    ("stage-04", "后期制作", ["14", "15", "16", "17", "18"]),
    ("stage-05", "最终交付与质量控制", ["19", "20"]),
]
EXPECTED_NAMES = [
    "项目管理与制片统筹", "创意开发与故事策划", "剧本开发与戏剧结构",
    "导演与整体视听表达", "制作设计与场景美术", "分镜与镜头设计",
    "摄影指导与镜头语言", "灯光设计与影调控制", "场面调度与表演空间设计",
    "视觉开发与整体视觉统一", "角色、场景与道具资产制作", "视觉执行编译与提示词工程",
    "视频与动态镜头生成", "动画、特效与镜头修复", "媒体管理与素材管理",
    "剪辑与叙事节奏", "调色与视觉统一", "声音设计与音乐制作",
    "标题、字幕与视觉包装", "最终成片输出与交付", "独立质量审查与最终放行",
]

def fail(message):
    raise ValueError(message)

def validate(root: Path):
    root = Path(root)
    config = json.loads((root / "config/categories.json").read_text(encoding="utf-8"))
    index = json.loads((root / "catalog/film-production-21-node-index.json").read_text(encoding="utf-8"))
    expected_ids = [f"{n:02d}" for n in range(21)]
    expected_set = set(expected_ids)

    if config.get("schema_version") != "1.1.0":
        fail("Unexpected taxonomy schema version")
    if index.get("framework_version") != "V0.1":
        fail("Node index must remain aligned to framework V0.1")

    stages = config.get("stages")
    index_stages = index.get("stages")
    expected_stage_records = [{"id": i, "name": n, "nodes": ids} for i, n, ids in EXPECTED_STAGES]
    if stages != expected_stage_records or index_stages != expected_stage_records:
        fail("Five stage definitions, names, order, or node boundaries differ from locked V0.1")
    if stages != index_stages:
        fail("Stage definitions differ between config and node index")

    nodes = index.get("nodes")
    if not isinstance(nodes, list) or len(nodes) != 21:
        fail("Node index must contain exactly 21 records")
    node_ids = [n.get("id") for n in nodes]
    if node_ids != expected_ids:
        fail("Node index must contain each canonical ID exactly once and in order")
    by_id = {n["id"]: n for n in nodes}
    for i, name in enumerate(EXPECTED_NAMES):
        node = by_id[expected_ids[i]]
        if node.get("name") != name:
            fail(f"Node {expected_ids[i]} name differs from locked V0.1")
        expected_stage = next(stage_id for stage_id, _, ids in EXPECTED_STAGES if expected_ids[i] in ids)
        if node.get("stage_id") != expected_stage:
            fail(f"Node {expected_ids[i]} has incorrect stage_id")
        for field in ("english_name", "mission", "primary_deliverables", "status"):
            if not isinstance(node.get(field), str) or not node[field].strip():
                fail(f"Node {expected_ids[i]} missing required field: {field}")

    categories = config.get("categories")
    if not isinstance(categories, list) or len(categories) != 21:
        fail("There must be exactly 21 primary node categories")
    category_ids = [c.get("id") for c in categories]
    if category_ids != [f"node-{n}" for n in expected_ids]:
        fail("Primary category IDs must map one-to-one to canonical node IDs")
    mapped = []
    for category in categories:
        node_id = category["nodes"][0] if isinstance(category.get("nodes"), list) and len(category["nodes"]) == 1 else None
        if node_id not in expected_set:
            fail(f"Category {category.get('id')} must map to exactly one valid node")
        mapped.append(node_id)
        node = by_id[node_id]
        if category.get("label") != f"{node_id} {node['name']}":
            fail(f"Category label mismatch for {node_id}")
        if category.get("stage_id") != node["stage_id"]:
            fail(f"Category stage mismatch for {node_id}")
        if not category.get("keywords"):
            fail(f"Category {node_id} has no discovery keywords")
    if mapped != expected_ids or len(set(mapped)) != 21:
        fail("Each canonical node must have exactly one primary category")

    domains = config.get("cross_cutting_domains")
    if not isinstance(domains, list) or not domains:
        fail("Cross-cutting domains must be explicitly declared")
    domain_ids = [d.get("id") for d in domains]
    if len(domain_ids) != len(set(domain_ids)) or set(domain_ids) & set(category_ids):
        fail("Cross-cutting domain IDs must be unique and separate from primary categories")
    for domain in domains:
        refs = domain.get("maps_to_nodes")
        if not isinstance(refs, list) or not refs or len(refs) != len(set(refs)) or not set(refs) <= expected_set:
            fail(f"Invalid node mapping for cross-cutting domain {domain.get('id')}")

    board_root = root / "library/21-nodes"
    if not board_root.is_dir():
        fail("Missing library/21-nodes directory")
    board_files = sorted(board_root.glob("??-*/README.md"))
    if len(board_files) != 21:
        fail(f"Expected exactly 21 board README files, found {len(board_files)}")
    for node_id in expected_ids:
        matches = list(board_root.glob(f"{node_id}-*/README.md"))
        if len(matches) != 1:
            fail(f"Node {node_id} must have exactly one knowledge board")
        text = matches[0].read_text(encoding="utf-8")
        if not re.search(rf"^# {node_id} — ", text, re.MULTILINE):
            fail(f"Board heading does not identify node {node_id}")

    for node in nodes:
        for rel in node.get("knowledge_entry_paths", []):
            if not (root / rel).is_file():
                fail(f"Node {node['id']} references missing knowledge entry: {rel}")

    return "PASS: locked V0.1 stage boundaries, 21 canonical nodes, one-to-one categories, cross-cutting mappings, 21 board files, and knowledge references."

if __name__ == "__main__":
    try:
        print(validate(Path(__file__).resolve().parents[1]))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)

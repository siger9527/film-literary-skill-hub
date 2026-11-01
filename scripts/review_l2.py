#!/usr/bin/env python3
"""Static L2 source-mechanism review for pinned GitHub Skill resources.

This tool reads repository trees and bounded text files. It never clones a
repository, installs dependencies, or executes untrusted source code.
Its findings are evidence-backed review leads, not proof of runtime behavior.
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
UA = "film-literary-skill-hub/0.1"
MAX_FILE_BYTES = 200_000
MAX_FILES_PER_REPOSITORY = 120
TEXT_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".yml", ".yaml", ".json", ".toml", ".md", ".txt", ".ps1", ".bat"}

def api_json(url):
    headers = {"Accept":"application/vnd.github+json","User-Agent":UA,"X-GitHub-Api-Version":"2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token: headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))

def raw_file(repo, commit, path):
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{urllib.parse.quote(path)}"
    req = urllib.request.Request(url, headers={"User-Agent":UA})
    with urllib.request.urlopen(req, timeout=20) as response:
        data = response.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("file exceeds 200 KB review limit")
    return data.decode("utf-8", "replace")

def classify_file(path):
    name = path.rsplit("/",1)[-1].lower()
    suffix = Path(name).suffix
    if name == "skill.md": return "skill_definition"
    if name.startswith("readme"): return "project_documentation"
    if name in {"license","licence"} or name.startswith(("license.","licence.")): return "license"
    if "test" in path.lower() or path.lower().startswith("tests/"): return "test"
    if name in {"pyproject.toml","requirements.txt","requirements-dev.txt","package.json","pnpm-lock.yaml","poetry.lock","uv.lock"}: return "dependency_manifest"
    if suffix in {".yml",".yaml",".json",".toml"}: return "configuration"
    if suffix in {".py",".js",".ts",".tsx",".jsx",".sh",".ps1",".bat"}: return "executable_source"
    if suffix in {".md",".txt"}: return "reference_documentation"
    return "other"

def inspect_text(path, text):
    findings = []
    patterns = [
        ("SUBPROCESS_EXECUTION", r"subprocess\.(run|Popen|call|check_call|check_output)"),
        ("SHELL_EXECUTION", r"\bos\.system\s*\(|shell\s*=\s*True"),
        ("DYNAMIC_CODE_EXECUTION", r"\b(eval|exec)\s*\("),
        ("NETWORK_ACCESS", r"\b(requests\.(get|post)|urllib\.request|httpx\.|fetch\s*\()"),
        ("FILE_DELETION", r"\b(shutil\.rmtree|os\.remove|os\.unlink)\s*\("),
        ("CREDENTIAL_ACCESS", r"(GITHUB_TOKEN|GH_TOKEN|API_KEY|SECRET|PASSWORD)"),
        ("PERMISSION_OR_APPROVAL", r"(approval|required_approval|checkpoint|permission|authorize)"),
        ("TEST_ASSERTION", r"\b(assert |assertEqual|assertRaises|expect\()"),
    ]
    for code, pattern in patterns:
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            lines = sorted({text.count("\n", 0, m.start()) + 1 for m in matches})[:20]
            findings.append({"code":code,"occurrences":len(matches),"line_numbers":lines})
    return findings

def review_resource(card, today=None):
    repo, commit = card["repository"], card["commit"]
    tree_data = api_json(f"{API}/repos/{repo}/git/trees/{commit}?recursive=1")
    if tree_data.get("truncated"):
        raise RuntimeError("recursive Git tree truncated; L2 review blocked")
    entries = [x for x in tree_data.get("tree",[]) if x.get("type") == "blob"]
    selected = []
    for entry in entries:
        path = entry["path"]
        kind = classify_file(path)
        if kind in {"skill_definition","project_documentation","license","test","dependency_manifest","configuration","executable_source","reference_documentation"}:
            selected.append((entry,kind))
    file_records, findings, errors = [], [], []
    if len(selected) > MAX_FILES_PER_REPOSITORY:
        errors.append({"path":"__repository__","error":f"selected file count {len(selected)} exceeds review cap {MAX_FILES_PER_REPOSITORY}"})
        selected = selected[:MAX_FILES_PER_REPOSITORY]
    for entry,kind in selected:
        path=entry["path"]
        if Path(path).suffix.lower() not in TEXT_SUFFIXES and kind not in {"skill_definition","project_documentation","license","dependency_manifest"}:
            file_records.append({"path":path,"kind":kind,"read":False,"reason":"non-text or unsupported extension"})
            continue
        try:
            body=raw_file(repo,commit,path)
            file_records.append({"path":path,"kind":kind,"read":True,"bytes":len(body.encode("utf-8"))})
            for item in inspect_text(path,body):
                findings.append({"path":path,**item})
        except Exception as exc:
            errors.append({"path":path,"error":str(exc)})
            file_records.append({"path":path,"kind":kind,"read":False,"reason":str(exc)})
    kind_counts={}
    for item in file_records: kind_counts[item["kind"]]=kind_counts.get(item["kind"],0)+1
    disposition = "BLOCKED" if errors else "L2_STATIC_REVIEW_COMPLETE"
    return {
        "repository":repo,"commit":commit,"skill_path":card["path"],
        "review_level":"L2","disposition":disposition,
        "tree_truncated":False,"files_indexed":len(entries),"files_selected":len(selected),
        "files_read":sum(1 for x in file_records if x["read"]),
        "file_kind_counts":kind_counts,"file_evidence":file_records,
        "mechanism_findings":findings,"review_errors":errors,
        "capability_claims_not_runtime_verified":True,
        "runtime_tested":False,"source_code_executed":False,
        "limitations":[
            "Static pattern findings are leads, not proof of exploitability or runtime behavior.",
            "No upstream code was executed and no dependencies were installed.",
            "Tests were indexed and inspected as text; their pass status was not independently established.",
            "License text and third-party assets require scoped legal review."
        ],
        "reviewed_at":dt.datetime.now(dt.timezone.utc).isoformat()
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",default=str(ROOT/"catalog/generated/resources.json"))
    parser.add_argument("--output",default=str(ROOT/"catalog/generated/l2-reviews.json"))
    parser.add_argument("--limit",type=int,default=10)
    parser.add_argument("--only-l1-candidates",action="store_true")
    args=parser.parse_args()
    payload=json.loads(Path(args.input).read_text(encoding="utf-8"))
    cards=payload.get("resources",[])
    if args.only_l1_candidates:
        l1=json.loads((ROOT/"catalog/generated/l1-reviews.json").read_text(encoding="utf-8"))
        eligible={(x["repository"],x["commit"],x["path"]) for x in l1["reviews"] if x["disposition"]=="L1_CANDIDATE"}
        cards=[x for x in cards if (x["repository"],x["commit"],x["path"]) in eligible]
    results=[]
    for card in cards[:max(0,args.limit)]:
        try: results.append(review_resource(card))
        except Exception as exc:
            results.append({
                "repository":card["repository"],"commit":card["commit"],"skill_path":card["path"],
                "review_level":"L2","disposition":"BLOCKED","tree_truncated":False,
                "files_indexed":0,"files_selected":0,"files_read":0,"file_kind_counts":{},
                "file_evidence":[],"mechanism_findings":[],
                "review_errors":[{"path":"__repository__","error":str(exc)}],
                "capability_claims_not_runtime_verified":True,
                "runtime_tested":False,"source_code_executed":False,
                "limitations":[
                    "Review blocked before source inspection completed.",
                    "No upstream code was executed and no dependencies were installed.",
                    "A BLOCKED result is not a safety or quality endorsement."
                ],
                "reviewed_at":dt.datetime.now(dt.timezone.utc).isoformat()
            })
        time.sleep(0.5)
    result={"review_level":"L2","generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
            "count":len(results),"reviews":results}
    target=Path(args.output); target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"reviewed":len(results),"blocked":sum(x["disposition"]=="BLOCKED" for x in results),
                      "output":str(target)},ensure_ascii=False))

if __name__=="__main__": main()

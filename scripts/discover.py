#!/usr/bin/env python3
"""Discover public GitHub repositories and index SKILL.md metadata. Never executes source code."""
from __future__ import annotations
import argparse, datetime as dt, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
USER_AGENT = "film-literary-skill-hub/0.1"

def request_json(url: str):
    headers = {"Accept":"application/vnd.github+json","User-Agent":USER_AGENT,"X-GitHub-Api-Version":"2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token: headers["Authorization"] = "Bearer " + token
    req=urllib.request.Request(url,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=25) as r: return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body=e.read().decode("utf-8","replace")
        raise RuntimeError(f"GitHub API {e.code} for {url}: {body[:400]}") from e

def get_repo(full_name):
    return request_json(f"{API}/repos/{full_name}")

def get_tree(full_name, sha):
    return request_json(f"{API}/repos/{full_name}/git/trees/{sha}?recursive=1")

def raw_text(full_name, sha, path):
    url=f"https://raw.githubusercontent.com/{full_name}/{sha}/{urllib.parse.quote(path)}"
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT})
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            data=r.read(200_001)
        if len(data)>200_000: return ""
        return data.decode("utf-8","replace")
    except Exception: return ""

def parse_frontmatter(text):
    result={}
    if not text.startswith("---"): return result
    parts=text.split("---",2)
    if len(parts)<3: return result
    for line in parts[1].splitlines():
        m=re.match(r"^([A-Za-z0-9_-]+):\\s*(.*?)\\s*$",line)
        if m: result[m.group(1)]=m.group(2).strip('"\\'')
    return result

def license_state(repo, sha, tree):
    candidates=[x["path"] for x in tree.get("tree",[]) if x.get("type")=="blob" and re.fullmatch(r"(?i)(license|licence)(\\.[a-z0-9]+)?",x["path"].split("/")[-1])]
    if not candidates: return "NO_LICENSE_FOUND", None
    # A root license is evidence, not proof that third-party assets are covered.
    root=next((p for p in candidates if "/" not in p),candidates[0])
    return "LICENSED_REVIEW_REQUIRED", root

def classify(name, description, content, categories):
    hay=(name+" "+description+" "+content[:5000]).lower()
    ranked=[]
    for c in categories["categories"]:
        score=sum(1 for kw in c["keywords"] if kw.lower() in hay)
        if score: ranked.append((score,c["id"]))
    return [x[1] for x in sorted(ranked,reverse=True)[:4]]

def discover_repositories(config, limit):
    found={}
    for q in config["queries"]:
        url=API+"/search/repositories?"+urllib.parse.urlencode({"q":q+" fork:false","sort":"updated","order":"desc","per_page":min(limit,30)})
        data=request_json(url)
        for item in data.get("items",[]): found[item["full_name"]]=item
        time.sleep(1)
    for name in config.get("seed_repositories",[]):
        try: found[name]=get_repo(name)
        except Exception as e: print(f"seed skipped {name}: {e}",file=sys.stderr)
    return found

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--limit",type=int,default=None)
    ap.add_argument("--output",default="catalog/generated")
    args=ap.parse_args()
    cfg=json.loads((ROOT/"config/sources.json").read_text("utf-8"))
    cats=json.loads((ROOT/"config/categories.json").read_text("utf-8"))
    repos=discover_repositories(cfg,args.limit or cfg["max_repositories_per_query"])
    out=ROOT/args.output; out.mkdir(parents=True,exist_ok=True)
    cards=[]; errors=[]
    for full_name,meta in sorted(repos.items()):
        try:
            commit=meta["default_branch"]
            branch=request_json(f"{API}/repos/{full_name}/branches/{urllib.parse.quote(commit,safe='')}")
            sha=branch["commit"]["sha"]
            tree=get_tree(full_name,sha)
            paths=[x["path"] for x in tree.get("tree",[]) if x.get("type")=="blob" and x["path"].split("/")[-1].lower()=="skill.md"]
            license_status,license_file=license_state(meta,sha,tree)
            for path in paths[:cfg["max_skill_files_per_repository"]]:
                body=raw_text(full_name,sha,path)
                fm=parse_frontmatter(body)
                skill_name=fm.get("name") or Path(path).parent.name or meta["name"]
                desc=fm.get("description") or meta.get("description") or ""
                cards.append({"repository":full_name,"commit":sha,"path":path,"skill_name":skill_name,"description":desc[:500],"source_url":f"https://github.com/{full_name}/blob/{sha}/{path}","license_status":license_status,"license_file":license_file,"review_status":"DISCOVERED","categories":classify(skill_name,desc,body,cats),"evidence":[f"Repository metadata: https://github.com/{full_name}",f"Commit-pinned Skill file: https://github.com/{full_name}/blob/{sha}/{path}"],"discovered_at":dt.datetime.now(dt.timezone.utc).isoformat()})
            time.sleep(.5)
        except Exception as e: errors.append({"repository":full_name,"error":str(e)})
    cards.sort(key=lambda x:(x["repository"],x["path"]))
    (out/"resources.json").write_text(json.dumps({"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),"count":len(cards),"resources":cards},ensure_ascii=False,indent=2)+"\\n","utf-8")
    lines=["# Discovered Skill Resources","",f"Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}","",f"Resources discovered: **{len(cards)}**","","> Discovery is not a quality review. License status is preliminary. No source code was executed.","","| Skill | Repository | Categories | License | Review |","|---|---|---|---|---|"]
    for c in cards:
        lines.append(f"| [{c['skill_name']}]({c['source_url']}) | [{c['repository']}](https://github.com/{c['repository']}) | {', '.join(c['categories']) or 'unclassified'} | {c['license_status']} | {c['review_status']} |")
    (out/"README.md").write_text("\\n".join(lines)+"\\n","utf-8")
    (out/"errors.json").write_text(json.dumps(errors,ensure_ascii=False,indent=2)+"\\n","utf-8")
    print(json.dumps({"repositories_checked":len(repos),"skills_found":len(cards),"errors":len(errors),"output":str(out)},ensure_ascii=False))
if __name__=="__main__": main()

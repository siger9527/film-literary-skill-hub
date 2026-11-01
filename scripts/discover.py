#!/usr/bin/env python3
"""Discover public GitHub repositories and index SKILL.md metadata. Never executes source code."""
from __future__ import annotations
import argparse, datetime as dt, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
USER_AGENT = "film-literary-skill-hub/0.1"

def request_json(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT, "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"GitHub API {exc.code} for {url}: {body[:400]}") from exc

def get_repo(full_name):
    return request_json(f"{API}/repos/{full_name}")

def get_tree(full_name, sha):
    tree = request_json(f"{API}/repos/{full_name}/git/trees/{sha}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("Git tree response was truncated; refusing to publish an incomplete repository scan")
    return tree

def raw_text(full_name, sha, path):
    url = f"https://raw.githubusercontent.com/{full_name}/{sha}/{urllib.parse.quote(path)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = response.read(200_001)
        if len(data) > 200_000:
            return None
        return data.decode("utf-8", "replace")
    except Exception:
        return None

def parse_frontmatter(text):
    result = {}
    if not text.startswith("---"):
        return result
    parts = text.split("---", 2)
    if len(parts) < 3:
        return result
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if match:
            result[match.group(1)] = match.group(2).strip('"\'')
    return result

def license_state(tree):
    candidates = [
        item["path"] for item in tree.get("tree", [])
        if item.get("type") == "blob"
        and re.fullmatch(r"(?i)(license|licence)(\.[a-z0-9]+)?", item["path"].split("/")[-1])
    ]
    root = next((path for path in candidates if "/" not in path), None)
    if root:
        return "LICENSED_REVIEW_REQUIRED", root
    if candidates:
        return "LICENSE_SCOPE_UNCLEAR", sorted(candidates)[0]
    return "NO_LICENSE_FOUND", None

def classify(name, description, content, categories):
    haystack = (name + " " + description + " " + content[:5000]).lower()
    ranked = []
    for category in categories["categories"]:
        score = sum(1 for keyword in category["keywords"] if keyword.lower() in haystack)
        if score:
            ranked.append((score, category["id"]))
    return [item[1] for item in sorted(ranked, reverse=True)[:4]]

def discover_repositories(config, limit):
    found = {}
    for query in config["queries"]:
        url = API + "/search/repositories?" + urllib.parse.urlencode({
            "q": query + " fork:false", "sort": "updated", "order": "desc", "per_page": min(limit, 30)
        })
        data = request_json(url)
        for item in data.get("items", []):
            found[item["full_name"]] = item
        time.sleep(1)
    for name in config.get("seed_repositories", []):
        try:
            found[name] = get_repo(name)
        except Exception as exc:
            print(f"seed skipped {name}: {exc}", file=sys.stderr)
    return found

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", default="catalog/generated")
    args = parser.parse_args()
    config = json.loads((ROOT / "config/sources.json").read_text("utf-8"))
    categories = json.loads((ROOT / "config/categories.json").read_text("utf-8"))
    repositories = discover_repositories(config, args.limit or config["max_repositories_per_query"])
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)
    cards, errors = [], []
    for full_name, metadata in sorted(repositories.items()):
        try:
            branch_name = metadata["default_branch"]
            branch = request_json(f"{API}/repos/{full_name}/branches/{urllib.parse.quote(branch_name, safe='')}")
            sha = branch["commit"]["sha"]
            tree = get_tree(full_name, sha)
            skill_paths = [
                item["path"] for item in tree.get("tree", [])
                if item.get("type") == "blob" and item["path"].split("/")[-1].lower() == "skill.md"
            ]
            license_status, license_file = license_state(tree)
            license_text = raw_text(full_name, sha, license_file) if license_file else None
            license_spdx = detect_spdx(license_text or "")
            for path in skill_paths[:config["max_skill_files_per_repository"]]:
                body = raw_text(full_name, sha, path)
                if body is None:
                    errors.append({"repository": full_name, "path": path, "error": "Skill file could not be read or exceeded 200 KB"})
                    body = ""
                frontmatter = parse_frontmatter(body)
                skill_name = frontmatter.get("name") or Path(path).parent.name or metadata["name"]
                description = frontmatter.get("description") or metadata.get("description") or ""
                cards.append({
                    "repository": full_name, "commit": sha, "path": path, "skill_name": skill_name,
                    "description": description[:500],
                    "source_url": f"https://github.com/{full_name}/blob/{sha}/{path}",
                    "license_status": license_status, "license_file": license_file, "license_spdx": license_spdx,
                    "license_evidence_url": f"https://github.com/{full_name}/blob/{sha}/{license_file}" if license_file else None,
                    "review_status": "DISCOVERED", "source_text_read": bool(body),
                    "categories": classify(skill_name, description, body, categories),
                    "evidence": [f"Repository metadata: https://github.com/{full_name}",
                                 f"Commit-pinned Skill file: https://github.com/{full_name}/blob/{sha}/{path}"],
                    "discovered_at": dt.datetime.now(dt.timezone.utc).isoformat()
                })
            time.sleep(0.5)
        except Exception as exc:
            errors.append({"repository": full_name, "error": str(exc)})
    cards.sort(key=lambda item: (item["repository"], item["path"]))
    generated = dt.datetime.now(dt.timezone.utc).isoformat()
    (output / "resources.json").write_text(
        json.dumps({"generated_at": generated, "count": len(cards), "resources": cards}, ensure_ascii=False, indent=2) + "\n",
        "utf-8"
    )
    lines = [
        "# Discovered Skill Resources", "", f"Generated: {generated}", "",
        f"Resources discovered: **{len(cards)}**", "",
        "> Discovery is not a quality review. License status is preliminary. No source code was executed.",
        "", "| Skill | Repository | Categories | License | Review |", "|---|---|---|---|---|"
    ]
    for card in cards:
        lines.append(
            f"| [{card['skill_name']}]({card['source_url']}) | "
            f"[{card['repository']}](https://github.com/{card['repository']}) | "
            f"{', '.join(card['categories']) or 'unclassified'} | {card['license_status']} | {card['review_status']} |"
        )
    (output / "README.md").write_text("\n".join(lines) + "\n", "utf-8")
    (output / "errors.json").write_text(json.dumps(errors, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps({"repositories_checked": len(repositories), "skills_found": len(cards),
                      "errors": len(errors), "output": str(output)}, ensure_ascii=False))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Conservative L1 metadata/structure triage. This is not a quality endorsement."""
from __future__ import annotations
import argparse, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def assess(card, today=None):
    today = today or dt.datetime.now(dt.timezone.utc).date()
    flags = []
    score = 100
    if not card.get("source_text_read", False):
        flags.append("SOURCE_UNREADABLE")
        score -= 35
    if not card.get("frontmatter_name_present", False):
        flags.append("FRONTMATTER_NAME_MISSING")
        score -= 10
    if not card.get("frontmatter_description_present", False):
        flags.append("FRONTMATTER_DESCRIPTION_MISSING")
        score -= 10
    if not card.get("readme_present", False):
        flags.append("README_MISSING")
        score -= 10
    if card.get("repository_archived", False):
        flags.append("REPOSITORY_ARCHIVED")
        score -= 20
    if card.get("license_status") == "NO_LICENSE_FOUND":
        flags.append("NO_LICENSE_FOUND")
        score -= 15
    elif card.get("license_status") == "LICENSE_SCOPE_UNCLEAR":
        flags.append("LICENSE_SCOPE_UNCLEAR")
        score -= 10
    pushed = card.get("repository_pushed_at")
    if pushed:
        try:
            pushed_date = dt.datetime.fromisoformat(pushed.replace("Z", "+00:00")).date()
            age_days = (today - pushed_date).days
            if age_days > 730:
                flags.append("REPOSITORY_STALE_OVER_2Y")
                score -= 10
            elif age_days > 365:
                flags.append("REPOSITORY_STALE_OVER_1Y")
                score -= 5
        except (ValueError, TypeError):
            flags.append("INVALID_PUSHED_AT")
            score -= 5
    else:
        flags.append("PUSHED_AT_UNKNOWN")
        score -= 5
    score = max(0, min(100, score))
    if not card.get("source_text_read", False):
        disposition = "BLOCKED"
    elif card.get("repository_archived", False) or card.get("license_status") == "NO_LICENSE_FOUND":
        disposition = "MANUAL_REVIEW_REQUIRED"
    elif score >= 80:
        disposition = "L1_CANDIDATE"
    else:
        disposition = "OBSERVE"
    return {
        "repository": card["repository"],
        "commit": card["commit"],
        "path": card["path"],
        "metadata_completeness_score": score,
        "disposition": disposition,
        "flags": flags,
        "review_level": "L1",
        "limitations": [
            "This score measures metadata and repository-structure completeness only.",
            "It does not measure Skill effectiveness, correctness, safety, or production readiness.",
            "No source code was executed and no runtime behavior was tested."
        ]
    }

def review_catalog(source, output):
    payload = json.loads(Path(source).read_text(encoding="utf-8"))
    reviews = [assess(card) for card in payload.get("resources", [])]
    result = {"review_level": "L1", "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
              "count": len(reviews), "reviews": reviews}
    Path(output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(reviews)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(ROOT / "catalog/generated/resources.json"))
    parser.add_argument("--output", default=str(ROOT / "catalog/generated/l1-reviews.json"))
    args = parser.parse_args()
    print(f"L1 reviews generated: {review_catalog(args.input, args.output)}")

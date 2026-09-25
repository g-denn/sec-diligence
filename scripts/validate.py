"""Repository contract validator. Uses only the Python standard library."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "sec-diligence"
REQUIRED_FILES = (
    "README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md", "PRODUCT_VISION.md", "TODO.md",
    "skills/sec-diligence/SKILL.md", "skills/sec-diligence/agents/openai.yaml",
    "skills/sec-diligence/references/source-hierarchy.md",
    "skills/sec-diligence/references/diligence-review-areas.md",
    "skills/sec-diligence/references/output-contract.md", "examples/sample-input.md",
    "examples/sample-output.md", ".claude-plugin/marketplace.json", ".github/workflows/validate.yml",
    "tests/fixtures/cases.json",
)
REQUIRED_OUTPUT_SECTIONS = (
    "# SEC filing evidence ledger", "**Scope:**", "**As of:**", "**Identity proof:**",
    "## Material disclosed risks", "**Fact:**", "**Inference:**", "**Calculation:**", "**Unknown:**",
    "## Open questions and coverage gaps", "## Sources reviewed", "**Citation:**",
)
UNSAFE_OUTPUT_LANGUAGE = re.compile(
    r"\b(buy|sell|hold|avoid|long|short|recommend(?:ation|ed|ing)?|fraud(?:ulent)?|scam)\b"
    r"|\b(?:composite|aggregate|overall)\s+(?:risk\s+)?(?:score|rating)\b",
    re.IGNORECASE,
)
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_frontmatter(errors: list[str]) -> None:
    content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not match:
        fail(errors, "SKILL.md has no YAML frontmatter")
        return
    frontmatter = match.group(1)
    if not re.search(r"^name:\s*sec-diligence\s*$", frontmatter, re.MULTILINE):
        fail(errors, "SKILL.md frontmatter name must be sec-diligence")
    description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not description or len(description.group(1).strip()) < 40:
        fail(errors, "SKILL.md needs a discriminating description")
    if "SEC accepted timestamp on or before" not in content:
        fail(errors, "SKILL.md must prevent post-cutoff evidence from entering historical reviews")


def check_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        for target in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#") or target.startswith("mailto:"):
                continue
            candidate = (path.parent / target.split("#", 1)[0]).resolve()
            if not candidate.exists():
                fail(errors, f"broken internal link in {path.relative_to(ROOT)}: {target}")


def check_output(errors: list[str], label: str, output: str) -> None:
    for required in REQUIRED_OUTPUT_SECTIONS:
        if required not in output:
            fail(errors, f"{label} missing output-contract token: {required}")
    if not re.search(r"\*\*As of:\*\*\s*\d{4}-\d{2}-\d{2}", output):
        fail(errors, f"{label} has no ISO as-of date")
    unsafe = UNSAFE_OUTPUT_LANGUAGE.search(output)
    if unsafe:
        fail(errors, f"{label} contains unsafe recommendation language: {unsafe.group(0)}")


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required file: {relative}")
    if errors:
        print("\n".join(errors))
        return 1
    check_frontmatter(errors)
    check_links(errors)
    try:
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid marketplace JSON: {exc}")
        marketplace = {}
    plugins = marketplace.get("plugins", []) if isinstance(marketplace, dict) else []
    expected_skill = "./skills/sec-diligence"
    if not any(
        isinstance(plugin, dict)
        and plugin.get("source") == "./"
        and plugin.get("strict") is False
        and expected_skill in plugin.get("skills", [])
        for plugin in plugins
    ):
        fail(errors, "marketplace must explicitly map ./skills/sec-diligence from the repository root")
    check_output(errors, "examples/sample-output.md", (ROOT / "examples/sample-output.md").read_text(encoding="utf-8"))
    try:
        cases = json.loads((ROOT / "tests/fixtures/cases.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"invalid fixture JSON: {exc}")
        cases = []
    if len(cases) < 4:
        fail(errors, "need at least four deterministic fixtures")
    expected = {"going-concern-runway", "dilution", "related-party-control-weakness", "clean-negative-control"}
    seen = {case.get("id") for case in cases if isinstance(case, dict)}
    if not expected.issubset(seen):
        fail(errors, "fixture set is missing a required scenario")
    for case in cases:
        if not isinstance(case, dict) or not case.get("synthetic"):
            fail(errors, "every fixture must be clearly marked synthetic")
            continue
        check_output(errors, f"fixture {case.get('id', '<unnamed>')}", str(case.get("output", "")))
    if errors:
        print("Validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Validation passed: repository structure, static output contract, links, fixtures, and safety-language checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

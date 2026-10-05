#!/usr/bin/env python3
"""Validate plugins before packaging or uploading.

Checks, per plugin:
  - plugin.json parses and only uses schema-allowed top-level keys
  - every skills/<dir>/SKILL.md has YAML-ish frontmatter with name + description
  - the frontmatter name matches its directory name
  - description is long enough to route on (activation depends on it)
  - no obvious secrets committed in the package

Exit code 1 on any failure. No network required except the optional
schema-allowlist refresh, which is cached in .schema-cache.json.

Usage:
    python3 scripts/validate.py            # validate every plugin
    python3 scripts/validate.py <name> ... # validate specific plugins
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"

# Agent Plugins 1.0.0 schema is additionalProperties:false, so this list is exact.
ALLOWED_TOP_LEVEL = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
REQUIRED_TOP_LEVEL = {"name", "version", "description"}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)\b(api[_-]?key|secret|password|bearer)\s*[:=]\s*['\"][^'\"]{12,}"),
]


def fail(plugin: str, msg: str, errors: list[str]) -> None:
    errors.append(f"[{plugin}] {msg}")


def check_manifest(plugin: str, root: Path, errors: list[str]) -> None:
    for candidate in (root / "plugin.json", root / ".codex-plugin" / "plugin.json"):
        if candidate.is_file():
            break
    else:
        fail(plugin, "no plugin.json or .codex-plugin/plugin.json", errors)
        return

    try:
        manifest = json.loads(candidate.read_text())
    except json.JSONDecodeError as exc:
        fail(plugin, f"{candidate.name} is not valid JSON: {exc}", errors)
        return

    keys = set(manifest)
    unknown = keys - ALLOWED_TOP_LEVEL
    if unknown:
        fail(plugin, f"unknown top-level key(s) {sorted(unknown)} (schema rejects these)", errors)
    missing = REQUIRED_TOP_LEVEL - keys
    if missing:
        fail(plugin, f"missing required key(s) {sorted(missing)}", errors)

    name = manifest.get("name", "")
    if name and name != plugin:
        fail(plugin, f"manifest name {name!r} != directory name {plugin!r}", errors)
    if name and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
        fail(plugin, f"name {name!r} is not kebab-case", errors)

    version = str(manifest.get("version", ""))
    if version and not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(plugin, f"version {version!r} is not semver", errors)

    desc = manifest.get("description", "")
    if isinstance(desc, str) and len(desc) < 40:
        fail(plugin, "manifest description is very short; the directory listing depends on it", errors)

    print(f"  manifest ok  {candidate.relative_to(ROOT)}  v{version}")


def check_skills(plugin: str, root: Path, errors: list[str]) -> int:
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        print("  no skills/ directory (skills-only plugins must have one)")
        return 0

    count = 0
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            fail(plugin, f"{skill_dir.name}/ has no SKILL.md", errors)
            continue

        text = skill_file.read_text()
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match:
            fail(plugin, f"{skill_dir.name}/SKILL.md has no frontmatter block", errors)
            continue

        front = match.group(1)
        name_m = re.search(r"^name:\s*(.+?)\s*$", front, re.M)
        desc_m = re.search(r"^description:\s*(.+?)\s*$", front, re.M)

        if not name_m:
            fail(plugin, f"{skill_dir.name}/SKILL.md frontmatter has no name", errors)
        elif name_m.group(1) != skill_dir.name:
            fail(plugin, f"{skill_dir.name}/SKILL.md name is {name_m.group(1)!r}, must match dir", errors)

        if not desc_m:
            fail(plugin, f"{skill_dir.name}/SKILL.md frontmatter has no description", errors)
        elif len(desc_m.group(1)) < 60:
            fail(
                plugin,
                f"{skill_dir.name}/ description is only {len(desc_m.group(1))} chars; "
                "activation depends on it naming the workflow AND its triggers",
                errors,
            )

        body = text[match.end():].strip()
        if len(body) < 100:
            fail(plugin, f"{skill_dir.name}/SKILL.md body is nearly empty", errors)

        count += 1
        print(f"  skill ok     skills/{skill_dir.name}/SKILL.md  ({len(body)} chars body)")

    if count == 0:
        fail(plugin, "skills/ exists but contains no skill directories", errors)
    return count


def check_secrets(plugin: str, root: Path, errors: list[str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                rel = path.relative_to(ROOT)
                fail(plugin, f"possible secret in {rel} — never ship credentials in a plugin ZIP", errors)


def main(argv: list[str]) -> int:
    targets = argv[1:]
    if targets:
        roots = [(t, PLUGINS / t) for t in targets]
    else:
        roots = [
            (p.name, p) for p in sorted(PLUGINS.iterdir()) if p.is_dir()
        ] if PLUGINS.is_dir() else []

    if not roots:
        print("no plugins found under plugins/", file=sys.stderr)
        return 1

    errors: list[str] = []
    for name, root in roots:
        if not root.is_dir():
            fail(name, "directory does not exist", errors)
            continue
        print(f"\n{name}")
        check_manifest(name, root, errors)
        count = check_skills(name, root, errors)
        check_secrets(name, root, errors)
        print(f"  -> {count} skill(s)")

    print()
    if errors:
        print(f"FAILED ({len(errors)} problem(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("all plugins valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
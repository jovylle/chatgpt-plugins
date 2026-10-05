# chatgpt-plugins

ChatGPT / Codex plugins I build and publish. Each plugin is a folder of
instructions ("skills") that ChatGPT can install and use on request.

## What a plugin is

A named folder of instruction files. No server, no API, no code running. ChatGPT
reads the skills and follows them when a request matches.

```text
plugins/<plugin-name>/
├── plugin.json              # name, version, description, presentation
└── skills/
    └── <skill-name>/SKILL.md   # one folder per workflow
```

## Plugins

| Plugin | Version | What it does |
|---|---|---|
| [`video-prompt-builder`](plugins/video-prompt-builder) | 0.2.0 | Keyframes, motion prompts, continuity-safe clip sequences, golden-hour dreamscape style |

## How a skill gets chosen

ChatGPT reads each skill's `description:` line to decide whether that skill
applies to the current request. That line is the trigger — it must name both the
workflow and the conditions that should fire it. The body then carries the
procedure. This is why `description` quality matters more than body length.

There is no slash-command mechanism. You can `@`-mention a plugin explicitly in a
Work chat, but a skill's activation is model-decided, not bound to a keyword.

## Layout

```text
plugins/                    # plugin sources — the source of truth
.agents/plugins/marketplace.json   # catalog so the desktop app / Codex can find them
scripts/validate.py         # schema + skill + secret checks (run before packaging)
scripts/package.sh          # build dist/<name>-<version>.zip
dist/                       # build artifacts, gitignored
```

## Work on a plugin

```bash
# edit under plugins/<name>/ — never edit the installed copy or a dist/ zip

python3 scripts/validate.py          # all plugins
python3 scripts/validate.py <name>   # one plugin
./scripts/package.sh                 # build zips for every plugin
./scripts/package.sh <name>          # one plugin
```

`validate.py` exits non-zero on: unknown top-level manifest keys (the Agent
Plugins schema is `additionalProperties: false`), name/dir mismatches,
non-semver versions, short or missing skill descriptions, empty skill bodies, and
possible secrets.

## Install locally for testing

```bash
# repo marketplace is read by the ChatGPT desktop app and Codex CLI
cp -R /Volumes/DevSSD/fore/lab/chatgpt-plugins/plugins/* ~/.codex/plugins/
```

Restart the ChatGPT desktop app, then Plugins Directory → `jovylle-plugins` →
install. Plugins install into a cache path, so re-copy after editing and restart.

Check what the CLI sees:

```bash
codex plugin marketplace list
```

> **Path gotcha:** `source.path` in a marketplace file resolves against the
> marketplace ROOT, not the marketplace file's own directory. For a personal
> marketplace the root is your home directory, so a plugin in `~/.codex/plugins/`
> must be referenced as `./.codex/plugins/<name>`.

## Publish

Skills-only plugins go up as a ZIP. Metadata and skill changes need a new ZIP and
a version bump; once published, hosted MCP tool changes are picked up
automatically without a new package.

Review for a skills-only plugin is light. MCP plugins additionally need reviewer
credentials, five positive and three negative test cases, and a video walkthrough.

**Skills/MCP is a one-way door.** OpenAI does not support adding an MCP server to
an existing skills-only plugin, nor changing an MCP server's URL. Decide before
packaging; if both are wanted, ship two plugins.

## Authoring notes

- Portable layout puts OpenAI-specific presentation under
  `extensions.com.openai.interface`. The older `.codex-plugin/plugin.json` with a
  flat `interface` key still works as a compatibility fallback.
- Allowed top-level `plugin.json` keys: `$schema, name, version, description,
  author, homepage, repository, license, keywords, extensions`. Nothing else.
- Skill frontmatter `name` must equal its directory name.
- Keep `SKILL.md` short and put long material in `references/` beside it.
- Don't add a script when plain instructions do the job.

Docs: <https://developers.openai.com/plugins/llms.txt> — append `.md` to any page
URL for a clean Markdown version.
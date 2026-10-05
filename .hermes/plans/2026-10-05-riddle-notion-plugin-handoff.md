# Handoff — `.riddle` → Notion → plot plugin

> New session start. Read this file first, then `PROJECTS.md` context as needed.
> Repo: `/Volumes/DevSSD/fore/lab/chatgpt-plugins` → https://github.com/jovylle/chatgpt-plugins

## Goal

Jov wants a ChatGPT plugin where he sends a short trigger phrase and it:

1. Checks his Notion database for the next pending Filipino riddle (`bugtong`)
2. Lets him pick one
3. Writes a good plot from the riddle he picked

His original sketch was typing `.riddle` then `.plot`.

---

## READ THIS FIRST — the architecture is not decided, and probably doesn't need to be

Jov observed that **his ChatGPT already has Notion connected**. That single fact
may remove the need for any MCP server at all.

The question that decides everything:

> **Can ChatGPT, with the plugin installed, query Jov's Notion riddle database
> using its own built-in Notion connection?**

### Test this BEFORE building anything

In a ChatGPT chat, with the Notion connection enabled:

1. Ask it to list the pages in the riddle database
2. See whether it can read the database without a plugin at all

**If YES** → this is a **skills-only plugin**. A `SKILL.md` that instructs ChatGPT
to use its native Notion access. Roughly 15 minutes of work, no server, no
hosting, no review burden.

**If NO** (ChatGPT's Notion connection can't reach that specific DB, or can't be
instructed from a skill) → you need the MCP path below.

### The constraint that shapes both paths

From the docs (plugin review requirements):

> "Do not instruct the model to invoke another plugin or connector to complete its
> operation; implement required dependencies within your plugin."

This blocks a skill from *calling* the Notion connector as a dependency. But it
does not necessarily block a skill from *directing* the model to use a connection
the user has already enabled in their own account. That distinction is exactly
what the test above resolves. Do not assume — verify.

---

## What is already built and must not be broken

`video-prompt-builder` v0.2.0 — **skills-only**, 4 skills, live on GitHub, CI green:

| Skill | Purpose |
|---|---|
| `video-prompt-builder` | single-clip motion prompts (original, Jov's) |
| `keyframe-builder` | the still-image anchor frame |
| `clip-sequence` | multi-clip continuity, handoff frames |
| `dreamscape-direction` | Jov's golden-hour house style |

Repo tooling already in place — use it, don't rebuild it:

```bash
cd /Volumes/DevSSD/fore/lab/chatgpt-plugins
python3 scripts/validate.py          # schema + skill + secret checks — run before every package
./scripts/package.sh                 # builds dist/<name>-<version>.zip
```

`validate.py` exits non-zero on unknown manifest keys (schema is
`additionalProperties: false`), name/dir mismatch, non-semver version, weak skill
descriptions, empty bodies, and possible secrets. CI runs the same checks on push.

---

## The one-way door — decide before packaging

> "Adding an MCP server to an existing skills-only plugin is not currently supported."
> "To change an existing MCP server's URL, contact support."

So **a plugin is either skills-only forever, or MCP from birth.** If the test
above says ChatGPT's native Notion access works, ship skills-only and never think
about MCP again. If it doesn't, `riddle-notion` must be created with `mcp.json`
from its very first commit.

Note this also means: **do not add the riddle skill to `video-prompt-builder`.**
That plugin is already skills-only and published. Add `plugins/riddle/` as its own
plugin.

---

## Path A — skills-only (try this first, ~15 min)

Create `plugins/riddle/` with `plugin.json` (`"capabilities": ["Instructions"]`)
and skills:

- `riddle-picker` — trigger description must name the workflow AND its triggers:
  *"Fetch the next pending riddle from Jov's Notion riddle database and present it
  for selection. Use when the user asks for a riddle, the next riddle, or to start
  a new riddle."*
- `plot-writer` — takes a chosen riddle, writes a plot. Must **refuse** to invent
  a plot for a riddle the user has not picked.

**The `.riddle` / `.plot` shortcut does not exist.** There is no slash-command
mechanism in ChatGPT plugins. Activation is model-decided from the skill
`description`, or the user `@`-mentions the plugin in a Work chat. Set the
descriptions well and ask for the workflow in plain language. Do not promise Jov a
literal dot-command.

## Path B — MCP-backed (only if the test fails)

Needs a public HTTPS streamable-HTTP MCP server exposing Notion tools.

**Do not start from scratch.** Jov already proved this transport end-to-end.
Read the existing plan first — it contains two hard-won traps that will cost hours
to rediscover:

`/Volumes/DevSSD/fore/lab/.hermes/plans/2026-10-04_004618-chatgpt-mcp-tunnel-runtime.md`

Established facts from that plan (verified 2026-10-03/04):

- `tunnel-client` 0.0.14 installed at `/opt/homebrew/bin/tunnel-client`
- Working tunnel: `mcp-smoke-test` = `tunnel_6ac115c05f488191b59832e31196fb3f`
- Working invocation shape:
  ```zsh
  export CONTROL_PLANE_TUNNEL_ID='tunnel_…'
  tunnel-client run \
    --mcp.server-url 'url=http://127.0.0.1:8931/mcp,channel=main' \
    --health.listen-addr 127.0.0.1:0
  ```
- Prototype MCP that already works: `mcp-chatgpt-tunnel/mcp_plain_server.py`
  (Python MCP SDK 2.x, `MCPServer` API — note `FastMCP` no longer exists)

**Trap 1 — `--embedded-mcp-stub` cannot be used for a ChatGPT connection.** The
stub advertises OAuth endpoints on `127.0.0.1`; `tunnel-client` refuses to register
them (`base URL must use https`) and ChatGPT discovery fails with
`MCP server/discover response was inconsistent`. Use a real MCP server with no
OAuth metadata. In ChatGPT the auth mode must be **No authentication / None**.

**Trap 2 — `--embedded-stateless-mcp-stub` does not exist in v0.0.14** despite
upstream docs advertising it. Trust `tunnel-client run --help`, not the website.

**Hermes venv** (the only interpreter with MCP SDK 2.x — system python3 has none):
```
/Users/jovyllebermudez/.hermes/installs/3709e212c21ce0dd/environments/9fe377acc114465ea094c1b6cb311161/venv/bin/python
```

**launchd constraint:** services must live under `~/fore/services/`, NOT
`/Volumes/DevSSD` — launchd cannot read DevSSD under TCC.

Also note for Path B: a public submission additionally requires serving the exact
challenge token at `/.well-known/openai-apps-challenge` on the MCP host.

---

## Current environment state (verified 2026-10-05)

| Thing | State |
|---|---|
| `chatgpt-plugins` repo | live, public, CI green, default branch `main` |
| `video-prompt-builder` | v0.2.0, published as skills-only, locally installed |
| Local personal marketplace | `~/.agents/plugins/marketplace.json` → `jovylle-personal` |
| Installed plugin copy | `~/.codex/plugins/video-prompt-builder` (must stay in sync with `plugins/`) |
| ChatGPT desktop app | installed at `/Applications/ChatGPT.app` |
| `codex` CLI | 0.154.0, reads the marketplace |
| `tunnel-client` | 0.0.14 installed (Path B only) |
| `ntn` (Notion CLI) | **not installed** |
| Hermes MCP servers | phase0, playwright, chrome-devtools, hindsight — **no Notion** |
| Hermes `NOTION_API_KEY` | not set (only needed if we build Hermes-side tooling, which Path A does not) |

**ChatGPT-side Notion connection:** Jov reports one already exists. This is the
load-bearing unknown for the whole task — see READ THIS FIRST.

---

## Definition of done

- [ ] The architecture fork is resolved by an actual test, not an assumption, and
      the decision is written down in the repo README
- [ ] Plugin lives at `plugins/<name>/`, NOT inside `video-prompt-builder`
- [ ] `python3 scripts/validate.py` passes
- [ ] `./scripts/package.sh` produces `dist/<name>-<version>.zip` with a single
      top-level directory containing `plugin.json`
- [ ] Tested in a fresh ChatGPT chat; activation confirmed with both a direct
      request ("give me the next riddle") and a negative one ("fix my CSS" must
      NOT trigger it)
- [ ] Jov is told plainly that `.riddle` / `.plot` as literal dot-commands are not
      available, and what the real invocation looks like
- [ ] Committed and pushed; CI green
- [ ] Row added to `/Volumes/DevSSD/fore/lab/PROJECTS.md`

## Notes for the next session

- Jov's plugins are creative-workflow tools, not infrastructure. He wants working
  artifacts fast, and he notices the difference between "verified" and "claimed".
- `scripts/validate.py` and the CI zip-root assertion were both tested against
  deliberately broken input — they genuinely fail. Trust them.
- Skill `description:` lines are the real activation mechanism. They matter more
  than skill body length.
- Docs: `https://developers.openai.com/plugins/llms.txt`, and append `.md` to any
  page URL for clean Markdown.
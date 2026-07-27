# YouTube Comment Analyzer — Docker Sandbox kit

A [Docker Sandbox](https://docs.docker.com/ai/sandboxes/) **mixin kit** that turns
a sandboxed Claude Code agent into a YouTube-comment analyst. It:

1. installs a small `yt-fetch` CLI (scrapes a video's comments — **no API key**), and
2. injects a Claude Code skill (`analyze-yt-comments`) that tells the agent how to
   fetch and analyze them.

Once the kit is loaded, you just ask the agent in natural language:

> Analyze the comments on https://www.youtube.com/watch?v=… — what stood out,
> product/blog ideas, and pain points.

The agent runs `yt-fetch`, then produces a report with three sections:
**👍 What stood out**, **💡 Product & blog ideas**, and **⚠️ Pain points**, each
backed by verbatim quotes. No `ANTHROPIC_API_KEY` is needed — the agent does the
analysis itself using its own model access.

## Layout

```
kit/
├── spec.yaml        # GENERATED mixin kit — writes the tool + skill via initFiles
├── build.py         # regenerates spec.yaml from the sources below
└── src/
    ├── yt-fetch     # the comment-scraping CLI (editable source)
    └── SKILL.md     # the agent skill (editable source)
```

> **No bundled binaries.** The kit does not ship any file under a `files/`
> directory. Instead, `spec.yaml` embeds the `yt-fetch` script and `SKILL.md`
> inline and writes them into the sandbox at startup via `commands.initFiles`
> (with the right paths and modes). Edit the sources in `src/` and run
> `python3 build.py` to regenerate `spec.yaml`.

## Use it

```bash
# From the host, create a sandbox with the kit (local path, for development):
sbx run claude --kit ./kit

# …or add it to a running sandbox (restarts the box, preserves state):
sbx kit add <sandbox-name> ./kit
```

Then, inside the sandbox chat, give the agent a YouTube URL and ask it to analyze
the comments. To fetch manually:

```bash
yt-fetch "https://www.youtube.com/watch?v=..." --limit 300   # human-readable
yt-fetch "https://www.youtube.com/watch?v=..." --json        # structured
```

## Share it

```bash
sbx kit validate ./kit                 # check well-formedness
sbx kit pack ./kit -o yt-analyzer.zip  # zip archive
sbx kit push ./kit <oci-ref>           # publish to an OCI registry
```

> Kit sources default to `docker.io/` only. To load a local kit or a git/OCI
> source elsewhere, adjust `sbx settings set kit.allowedSources`.

## How it works / notes

- **Files** (`spec.yaml` → `commands.initFiles`): writes `yt-fetch` to
  `~/.local/bin` (mode `0755`) and `SKILL.md` to `~/.claude/skills/…` (mode
  `0644`) at startup from inline content — nothing is bundled or copied from a
  `files/` directory.
- **Install** (`spec.yaml` → `commands.install`): `python3 -m pip install --user`
  of `youtube-comment-downloader` (the base has system pip but no `venv`), and
  puts `~/.local/bin` on `PATH` via the persistent env file so the agent's shells
  resolve the command.
- **Network** (`network.allowedDomains`): YouTube (scraping) and PyPI (install).
  Nothing else.
- **Skill scope**: written to `~/.claude/skills/` (home scope) so it's available
  in every workspace in the sandbox.
- **Timezone**: the tool forces a valid `TZ` in-process — some sandboxes preset
  `TZ` to a non-zoneinfo value (e.g. `EDT4`) that would otherwise crash the
  comment parser.
- Scraping is best-effort; YouTube can rate-limit or change endpoints.

## Regenerating

```bash
python3 build.py   # re-embeds src/yt-fetch and src/SKILL.md into spec.yaml
```

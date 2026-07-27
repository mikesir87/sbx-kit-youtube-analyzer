# YouTube Comment Analyzer

A [Docker Sandbox](https://docs.docker.com/ai/sandboxes/) kit that turns a sandboxed Claude Code agent into a YouTube-comment analyst — no API key required.

## What it does

Load the kit, give the agent a YouTube URL, and ask it to analyze the comments. It produces a three-section report:

- 👍 **What stood out** — what viewers liked or reacted positively to
- 💡 **Product & blog ideas** — capabilities people are asking about, topics worth writing about
- ⚠️ **Pain points** — problems and frustrations, each tagged with severity

Comments are scraped directly from YouTube (no Google API key). The agent does the analysis itself using its own model access.

## Quick start

```bash
# Create a new sandbox with the kit loaded
sbx run claude --kit ./kit
```

Then in the sandbox chat:

> Analyze the comments on https://www.youtube.com/watch?v=…

## What's installed

| Component | What it does |
| --------- | ------------ |
| `yt-fetch` CLI | Scrapes a video's most-popular comments |
| `analyze-yt-comments` skill | Tells the agent how to fetch and structure the analysis |

See [`kit/README.md`](kit/README.md) for full details on the kit layout, how to build/validate/publish it, and implementation notes.

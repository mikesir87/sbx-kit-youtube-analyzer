#!/usr/bin/env python3
"""Generate spec.yaml for the yt-comment-analyzer Docker Sandbox kit.

Kits currently have a bug packaging bundled binaries under files/, so instead of
shipping the yt-fetch script and SKILL.md as static files, we embed their
contents inline in the kit's `commands.initFiles` block. Those files are written
into the sandbox at startup with the right paths and modes — no bundled binary.

This script keeps the script/skill as editable sources under src/ and stamps
them into spec.yaml with correct YAML literal block scalars.

    python3 build.py            # regenerate spec.yaml
"""

from __future__ import annotations

import pathlib

import yaml

HERE = pathlib.Path(__file__).parent
YT_FETCH = (HERE / "src" / "yt-fetch").read_text()
SKILL_MD = (HERE / "src" / "SKILL.md").read_text()

YT_FETCH_PATH = "/home/agent/.local/bin/yt-fetch"
SKILL_PATH = "/home/agent/.claude/skills/analyze-yt-comments/SKILL.md"


class LiteralStr(str):
    """A str subclass that YAML dumps as a literal block scalar (|)."""


def _literal_representer(dumper: yaml.Dumper, data: LiteralStr):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style="|")


yaml.add_representer(LiteralStr, _literal_representer)

spec = {
    "schemaVersion": "1",
    "kind": "mixin",
    "name": "yt-comment-analyzer",
    "displayName": "YouTube Comment Analyzer",
    "description": (
        "Installs a yt-fetch tool and a Claude Code skill for analyzing the "
        "comments on a YouTube video (typically a Docker product video) — what "
        "stood out, product & blog ideas, and pain points. No API key required; "
        "the agent does the analysis itself."
    ),
    # Outbound network contract: YouTube (scraping) + PyPI (the one dependency).
    "network": {
        "allowedDomains": [
            "www.youtube.com",
            "youtube.com",
            "pypi.org",
            "files.pythonhosted.org",
        ]
    },
    "commands": {
        # Files are written at startup from inline content — nothing is bundled.
        "initFiles": [
            {"path": YT_FETCH_PATH, "mode": "0755", "content": LiteralStr(YT_FETCH)},
            {"path": SKILL_PATH, "mode": "0644", "content": LiteralStr(SKILL_MD)},
        ],
        "install": [
            {
                "command": (
                    "python3 -m pip install --user --break-system-packages "
                    "youtube-comment-downloader"
                ),
                "user": "1000",
                "description": "Install youtube-comment-downloader",
            },
            {
                "command": (
                    "grep -qF '.local/bin' /etc/sandbox-persistent.sh 2>/dev/null || "
                    "echo 'export PATH=\"$HOME/.local/bin:$PATH\"' "
                    ">> /etc/sandbox-persistent.sh"
                ),
                "user": "1000",
                "description": "Put ~/.local/bin on PATH",
            },
        ],
    },
    "agentContext": LiteralStr(
        "A `yt-fetch <youtube-url>` command is installed for scraping a video's\n"
        "comments (no API key needed). To analyze a video's comments for product\n"
        'insight, use the "analyze-yt-comments" skill.\n'
    ),
}

HEADER = (
    "# GENERATED FILE — do not edit by hand.\n"
    "# Edit src/yt-fetch or src/SKILL.md and run `python3 build.py` to regenerate.\n"
)

out = HERE / "spec.yaml"
out.write_text(HEADER + yaml.dump(spec, sort_keys=False, width=1000, allow_unicode=True))
print(f"wrote {out} ({out.stat().st_size} bytes)")

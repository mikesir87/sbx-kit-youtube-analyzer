---
name: analyze-yt-comments
description: Analyze the YouTube comments on a video (typically about a product) to surface what users liked / what stood out, potential product & blog ideas, and pain points. Use when the user provides a YouTube URL and asks to analyze, summarize, or mine its comments for feedback or product insights.
---

# Analyze YouTube comments

Mine the comments on a YouTube video for actionable product signal. This skill
is for videos about products, but works for any video.

## When to use

Trigger when the user provides a YouTube URL (or video ID) and asks to analyze,
summarize, or extract insights/feedback/pain points from its comments.

## Steps

1. **Fetch the comments** with the installed `yt-fetch` tool:

   ```bash
   yt-fetch "<youtube-url>" --limit 300
   ```

   - Default limit is 300 of the most-popular comments; raise or lower it if the
     user asks (e.g. `--limit 500`). More comments = more signal but a longer read.
   - The tool prints the video title, canonical URL, and numbered comments.
   - If it errors (YouTube rate-limiting or comments disabled), report the error
     to the user and suggest retrying or lowering `--limit`. Do not fabricate
     comments.

2. **Analyze the fetched comments yourself.** Read strictly what is in the
   comments — do not invent feedback that isn't there, and do not rely on outside
   knowledge of the product. Organize findings into exactly these three buckets:

   - **👍 What stood out** — what users liked or reacted positively to.
   - **💡 Product & blog ideas** — capabilities users are asking for or curious
     about (often phrased as "does it support X / can it do Y?"), and topics the
     team could write about because interest is clearly there.
   - **⚠️ Pain points** — problems, confusion, bugs, or frustrations. Tag each
     with a rough severity (high / medium / low).

3. **Write the report** as Markdown with those three sections. For every finding:
   - Give it a short label and a one–two sentence description.
   - Include a few **short verbatim quotes** from the comments as evidence.
   - Prefer specific, substantive comments over generic praise.
   - If a bucket genuinely has nothing in it, say so rather than padding it.

   Start the report with the video title, the number of comments analyzed, and a
   2–4 sentence overall-sentiment summary.

## Notes

- `yt-fetch` needs no API key. It scrapes comments directly (YouTube and PyPI
  must be allowed in the sandbox network policy — the kit adds those rules).
- Scraping is best-effort; YouTube can rate-limit or change its endpoints.
- Use `yt-fetch "<url>" --json` if you want structured output to post-process.

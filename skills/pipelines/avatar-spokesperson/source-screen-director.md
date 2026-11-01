# Source Screen Director - Avatar Spokesperson Source Commentary

## When To Use

Use this stage after candidate discovery and before local media work.

## Process

1. Fetch transcript or transcript metadata for shortlisted videos.
2. Classify audio suitability by transcript word count:

| Word Count | Classification | Default Action |
| ---: | --- | --- |
| 0-30 | ideal_visual_first | Prefer for commentary |
| 31-80 | usable_light_speech | Mute or duck original audio |
| 81+ | narration_heavy | Skip unless doing recap/response |

3. Scrape comments for the final candidate when quota allows:
   - 50 comments minimum for normal candidates,
   - 100 comments for high-priority candidates.
4. Extract repeated viewer themes:
   - confusion points,
   - jokes and memes,
   - suspected tricks,
   - named moments,
   - questions about rules,
   - debate or controversy.
5. Propose source audio treatment: mute, duck, keep reaction hits, or reject.

## How To Fetch Comments

There is no registered comments tool. Use, in order:

1. **SocialKit REST** — `GET https://api.socialkit.dev/youtube/comments`
   with `url`, `limit=100`, `sortBy=top`; auth via `x-access-key` header
   (`SOCIALKIT_API_KEY`). Send a browser `User-Agent` — the default Python UA
   is blocked by Cloudflare (403). A 403 with `insufficient_credits` means quota
   is exhausted; the body includes `reset_at`.
2. **yt-dlp fallback (free)** — when SocialKit is out of credits:
   `yt-dlp --skip-download --write-comments --extractor-args
   "youtube:comment_sort=top;max_comments=150,all,0" -o <artifacts>/ytdlp_<name> <url>`
   then read `comments` (top-level: `parent == "root"`) from the `.info.json`.

Save raw comments to `artifacts/comments_<name>.json`. Record which fetcher was used.

## Comments Feed The Script

Comment mining is not a formality. Rank comments by likes and carry the top
themes into the script stage as audience intelligence:

- the moment viewers name most (that beat deserves the biggest reaction),
- the dominant joke/reference (use the feeling, do not copy the joke verbatim),
- the skeptic take (a one-line acknowledgement adds credibility),
- the line that best captures "why this matters" for the closer.

When screening several finalists, compare them on transcript classification
AND comment energy (likes on the top comments, not just views).

## Output

Write `source_screen` with transcript word count, classification, comment count,
comment themes, and recommended audio treatment.

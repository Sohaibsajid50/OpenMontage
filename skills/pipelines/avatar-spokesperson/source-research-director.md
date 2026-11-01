# Source Research Director - Avatar Spokesperson Source Commentary

## When To Use

Use this stage to find candidate source videos that have already proven audience
retention through high views or engagement.

## YouTube Search Policy

For YouTube discovery, use the SocialKit REST API path instead of the MCP search
wrapper when ranking by virality is needed.

Required REST parameters:

```text
type=shorts
sortBy=views
limit=10 or higher
query=<keyword pack entry>
```

After the REST response, locally sort candidates by numeric view count. The API
can expose `sortBy=views`, but production selection should not rely blindly on
returned order.

Use the MCP after search for enrichment when useful:

- transcript
- comments
- summary

## Process

1. Expand the user's keyword into 3-5 nearby search phrases.
2. Search YouTube Shorts first with REST `sortBy=views`.
3. Record raw results, request parameters, and local sorted order.
4. Keep at least 5 candidates when quota allows.
5. Shortlist candidates with strong visual title terms: `game`, `challenge`,
   `race`, `funny`, `family`, `kids`, `bottle`, `balloon`, `cup`, `dice`.
6. Present the shortlist for approval before downloading or spending generation
   budget unless the user has already chosen a source.

## Output

Write `source_research` with:

- query pack,
- REST request parameters,
- candidate URLs,
- title,
- channel,
- duration,
- views,
- likes/comments when available,
- source rank after local sorting,
- initial reason for shortlist.

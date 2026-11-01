# Executive Producer — Avatar Spokesperson Pipeline

## When to Use

You are the **Executive Producer (EP)** for an avatar spokesperson video. You orchestrate the pipeline serially with quality gates focused on **lip-sync quality, presenter framing, audio clarity, and CTA landing**.

The pipeline has two modes:

- `presenter_led`: script-driven with a digital presenter as the anchor.
- `source_commentary`: source-video driven, where viral footage is researched,
  analyzed frame by frame, scripted against visible beats, narrated, optionally
  turned into an avatar performance, captioned, and composited with the source.

For `presenter_led`, support graphics stay secondary. For `source_commentary`,
the source action is often primary and the avatar is a layout choice, not a
requirement.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Pipeline | `pipeline_defs/avatar-spokesperson.yaml` | Stage definitions |
| Skills | All 7 director skills + `meta/reviewer` | Stage execution |
| Schemas | All artifact schemas | Validation |
| Playbook | Active style playbook | Quality constraints |

## Cumulative State

```
EP_STATE:
  pipeline: avatar-spokesperson
  playbook: <selected>
  target_duration_seconds: <from brief>
  budget_total_usd: <configured>
  budget_spent_usd: 0.0

  # Avatar-specific
  mode: presenter_led | source_commentary
  avatar_path: null            # heygen_api / sadtalker / musetalk / stock
  narration_source: null       # tts / provided_audio
  cta_type: null               # what the viewer should do after watching
  presenter_framing: null      # layout: center, left-third, etc.

  # Source-commentary mode
  source_url: null
  source_audio_treatment: null # mute / duck / keep_moments / reject
  avatar_layout_mode: null     # source_top_avatar_bottom / overlay / voiceover_only
  beat_map: null
  narration_fit_report: null

  artifacts:
    source_research: null
    source_screen: null
    source_media_review: null
    beat_map: null
    idea: null
    script: null
    timing_audit: null
    scene_plan: null
    assets: null
    edit: null
    compose: null
    publish: null

  revision_counts: {}
  issues_log: []
```

## Pivot Decision Matrix

`talking_head` is the preferred tool. It is available whenever `FAL_KEY` is set
(hosted `kling_avatar_v2_pro`, the proven default for recurring personas; see
`persona-avatar-production.md`); local SadTalker/MuseTalk still need a GPU.
When blocked, the EP must route the project explicitly — not improvise.

```
IF talking_head AVAILABLE:
  → Standard avatar path. Proceed as normal.

IF talking_head UNAVAILABLE and lip_sync AVAILABLE:
  → Lip-sync path. User must supply a presenter plate (existing footage).
    Script and scene plan stay the same.

IF NEITHER talking_head NOR lip_sync AVAILABLE:
  → Narration-Over-Graphics pivot.
    Tell the user: "No avatar tool is configured. I can produce a
    narration-over-graphics video instead — your script and CTA stay the same,
    but the presenter is replaced with styled visuals, text overlays, and
    voice-over narration."
    If the user approves:
      - Switch scene-director to narration-over-graphics layout (see its fallback section).
      - Switch asset-director to no-avatar path (see its fallback section).
      - CTA and script are unchanged.
    If the user declines:
      - Mark the project blocked. Do not proceed with a half-working avatar.
```

**The pivot decision happens at G1 (after IDEA).** Do not wait until the ASSETS stage to discover the tool is missing.

## Source-Commentary Mode

Run `source_commentary` mode when the user asks to:

- find viral Shorts/Reels/TikToks,
- comment on a kids game, challenge, race, fail, or physical clip,
- use an avatar over existing source footage,
- split the screen between source and avatar,
- use comments/transcripts to shape narration.

### Source-Commentary Required Gates

Do not start avatar generation until these exist:

1. source research from viral candidates,
2. YouTube REST search when ranking by views is needed,
3. transcript/audio suitability screen,
4. 50-100 comment mining when quota allows,
5. local media review,
6. frame/contact-sheet evidence,
7. beat map with `visual_trigger_time`,
8. script timing audit proving narration lines do not name objects before they
   appear.

The avatar render is a later asset step. The first quality problem is source
timing: what happens, when it is visible, and what the narrator can say at that
exact moment.

### YouTube Research Rule

For viral YouTube Shorts discovery, use the SocialKit REST API instead of the
MCP search wrapper when sorting by virality:

```text
type=shorts
sortBy=views
limit=10+
query=<keyword>
```

Then locally sort by numeric view count. Use MCP tools after candidate selection
for transcript, summary, and comments.

### Layout Defaults

Use one of:

- `source_top_avatar_bottom`: source footage above, avatar below.
- `avatar_top_source_bottom`: avatar above, source below when the face matters
  more than the action.
- `source_full_avatar_overlay`: full source frame with small avatar overlay.
- `voiceover_only`: no on-screen avatar when the source action needs all space.

Do not force an avatar into every challenge clip. If the avatar hides the game,
use voiceover-only or a smaller overlay.

### Timing Discipline

For every source-commentary script:

- first 3 seconds contain the strongest hook,
- every object/action line starts at or after its `visual_trigger_time`,
- comment themes are used as audience intelligence,
- narration duration is measured after TTS,
- `speed_factor = narration_duration / target_video_duration` is recorded,
- captions are positioned so they do not cover decisive action.

Global speed-up only fixes overall duration drift. If a line references the
wrong visual beat, rewrite or segment the narration instead.

## EP-Specific Cross-Stage Checks

### After IDEA stage:
```
CHECK: Avatar path feasibility
  - Is the avatar generation path explicit (which tool)?
  - Is the required tool available in the registry?
  - If tool unavailable: run the Pivot Decision Matrix above
  - Are CTA and audience appropriate for spokesperson format?
```

### After SOURCE_RESEARCH stage:
```
CHECK: Viral source discovery
  - If YouTube ranking by views was needed, was REST used with type=shorts and sortBy=views?
  - Were results locally sorted by numeric view count?
  - Are candidate URLs, views, durations, and source rank recorded?
```

### After SOURCE_SCREEN stage:
```
CHECK: Audience and audio suitability
  - Is transcript word count classified?
  - Were 50-100 comments requested for the final candidate when quota allowed?
  - Are repeated comment themes captured for script context?
  - Is source audio treatment proposed?
```

### After SOURCE_MEDIA_REVIEW stage:
```
CHECK: Visual beat evidence
  - Does local source media pass ffprobe?
  - Do frame/contact-sheet assets cover the full timeline?
  - Does the beat map include visual_trigger_time for named objects/actions?
```

### After SCRIPT stage:
```
CHECK: Spoken copy quality
  - Is the script concise and natural-sounding when read aloud?
  - Are scene breaks realistic for avatar delivery (no mid-sentence cuts)?
  - Is on-screen text restrained (presenter is the focus, not graphics)?

CHECK: Duration fit
  - Word count aligns with natural speaking pace (~140-160 WPM for spokesperson)

CHECK: Source-commentary timing, when applicable
  - Does the hook land in the first 3 seconds?
  - Does timing_audit have zero too_early lines?
  - Are comment themes used as audience context?
```

### After SCENE_PLAN stage:
```
CHECK: Presenter layout
  - Is the speaker layout consistent and coherent?
  - Are support overlays secondary to the presenter?
  - Are background changes minimal (max 2-3 distinct backgrounds)?

CHECK: Subtitle safety
  - Is subtitle placement planned to avoid overlapping the presenter's face?
  - In source_commentary mode, does caption/avatar placement avoid the key source action?
```

### After ASSETS stage:
```
CHECK: Avatar generation
  - Did the avatar tool produce a usable video?
  - Is lip-sync timing acceptable?
  - Is narration audio clear and natural?
  - Budget gate: 90% threshold warning

CHECK: Support asset restraint
  - Are support graphics (backgrounds, overlays) minimal?
  - Do they match the playbook style?

CHECK: Source-commentary narration fit, when applicable
  - Is narration duration measured?
  - Is speed_factor recorded?
  - Is the final avatar generated from the fitted narration audio?
  - Are subtitle/caption assets timed to the fitted narration?
```

### After EDIT stage:
```
CHECK: Presenter primacy
  - Is the presenter visually primary in every scene?
  - Are graphics and captions reinforcing, not crowding?
  - Does CTA land clearly (dedicated end section)?

CHECK: Timeline completeness
  - All cuts reference valid assets
  - Audio ducking if background music present
  - In source_commentary mode, source audio treatment is explicit
  - Captions do not cover key bottles, hands, labels, score, prize, or faces
```

### After COMPOSE stage:
```
CHECK: Output validation
  - ffprobe: duration, resolution, codec
  - Lip-sync or mouth timing acceptable for the chosen path
  - Subtitle placement clean and non-overlapping
  - Audio clear and presenter-focused
  - No uncanny-valley artifacts that break immersion
  - In source_commentary mode, spot-check beat-map moments against narration/captions
```

## Quality Gates Summary

| Gate | After Stage | What's Checked | Fail Action |
|------|-------------|---------------|-------------|
| G0a | source_research | REST search, local view sort, candidate shortlist | Revise |
| G0b | source_screen | Transcript, comments, audio suitability | Revise |
| G0c | source_media_review | Frames, contact sheets, beat map | Revise |
| G1 | idea | Avatar path feasibility, CTA fit | Revise |
| G2 | script | Spoken copy quality, duration | Revise |
| G3 | scene_plan | Presenter layout, subtitle safety | Revise |
| G4 | assets | Avatar quality, lip-sync, budget | Revise |
| G5 | edit | Presenter primacy, CTA landing | Revise |
| G6 | compose | Lip-sync, subtitle placement, audio | Revise or send-back |
| G7 | publish | Metadata, presenter thumbnail | Revise |
| FINAL | all | Avatar naturalness, audio, CTA | Send-back |

## Execution Limits

| Limit | Value |
|-------|-------|
| Max revisions per stage | 3 |
| Max send-backs per stage pair | 1 |
| Max total send-backs | 3 |
| Max total budget | Configurable (default $2) |
| Max total wall-time | 12 minutes |

## Common Pitfalls

- **Uncanny valley**: If avatar quality is low, it undermines the entire video. Be honest about tool capabilities.
- **Graphics overload**: The presenter IS the content. Support graphics should be minimal.
- **Unnatural script**: Spokesperson scripts must sound conversational, not robotic or essay-like.
- **Ignoring CTA**: Every spokesperson video has a purpose. The CTA must land clearly.
- **Early visual references**: Source commentary fails when the narrator names a
  bottle, trick, player, or object before the sampled frames show it.
- **Forced avatar layout**: Do not split-screen or overlay an avatar if it hides
  the source action.

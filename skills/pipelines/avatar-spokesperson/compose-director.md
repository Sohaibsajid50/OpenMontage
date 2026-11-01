# Compose Director - Avatar Spokesperson Pipeline

## When To Use

Render the final spokesperson outputs. The bar is simple: the presenter must look stable, speech must be clear, and subtitles or support cards must not crowd the frame.

In `source_commentary` mode, render the source video plus narration, captions,
and optional avatar layout. The source action and avatar speech must stay timed
to the beat map.

## Runtime Routing (HARD CONSTRAINT — Remotion only)

Applies to presenter mode. `source_commentary` layouts render with the ffmpeg
renderers in `scripts/avatar_commentary/` (see "1. Render The Hero Cut First"), not Remotion.

Phase 1 deferred from HyperFrames. `edit_decisions.render_runtime` must be `"remotion"`. This pipeline depends on the Remotion `TalkingHead` composition and `remotion_caption_burn` — both have no HyperFrames parity in Phase 1.

- If `edit_decisions.render_runtime == "hyperframes"`, stop. Re-open the idea stage and surface the constraint. Silent rewrite is a governance violation.
- Per AGENT_GUIDE.md → "Present Both Composition Runtimes (HARD RULE)": the lock to remotion is NOT an excuse to skip the conversation. The user deserves to know that HyperFrames exists as a runtime and why it isn't viable for avatar-spokesperson. Log a `render_runtime_selection` decision with hyperframes `rejected_because: "TalkingHead + caption parity deferred on avatar-spokesperson"`.
- Pass `proposal_packet`/`brief` to `video_compose.execute()` for in-tool runtime-swap detection.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | What to render |
| Tools | `video_compose`, `audio_mixer`, `video_stitch`, `audio_enhance` | Render and audio finishing |
| Playbook | Active style playbook | Typography and layout rules |

## Process

### 1. Render The Hero Cut First

Prefer one strong master before derivatives. Compose:

- presenter video,
- subtitles,
- lower-thirds,
- CTA cards,
- mixed narration.

For source-commentary layouts, use the shared renderers in
`scripts/avatar_commentary/` (they read `artifacts/edit_decisions.json` and
`artifacts/voice_lines.json`; this ffmpeg build has no drawtext/libass, so
captions are PNG cards):

```bash
AVATAR_PROJECT=projects/<name> python scripts/avatar_commentary/render_split.py    # source_top_avatar_bottom
scripts/avatar_commentary/cut_person.sh projects/<name> projects/<name>/assets/video/<avatar>.mp4
AVATAR_PROJECT=projects/<name> python scripts/avatar_commentary/render_cutout.py   # source_full_avatar_cutout
AVATAR_PROJECT=projects/<name> python scripts/avatar_commentary/render_bubble.py   # circle facecam
```

### 2. Keep The Frame Clean

Subtitle and CTA placement matter more here than flashy transitions. Leave the face and mouth region unobstructed.

Check the persona's crop on real frames at 3–4 moments before the full render:
a first split render once cut Mason's mouth off (fixed by moving the crop).
Render a 7-frame spot-check sheet at the beat-map moments and confirm loudness
lands near -14 LUFS (`ebur128`).

### 3. Verify Mouth Timing And Audio

If the avatar path used lip sync or audio-driven talking head, check:

- mouth timing,
- face artifacts,
- drift on long sections,
- audio clarity.

### 4. Verify Every Output

Record important findings in:

- `render_report.verification_notes`
- `render_report.warnings`
- `render_report.metadata.variant_notes`

For source commentary, also record:

- duration match between source, narration, and final render,
- speed_factor used,
- caption placement notes,
- beat-map spot checks,
- whether each named object/action appears before or during the matching line.

### 5. Quality Gate

- the output file is valid,
- speech is clear,
- subtitles stay readable,
- the presenter remains visually stable.
- source-commentary captions do not hide decisive source action,
- split-screen or overlay avatar does not block the game mechanics.

## Common Pitfalls

- Letting subtitles cover the chin or mouth area.
- Shipping a long lip-sync render without spot-checking drift.
- Making derivative crops that cut off the presenter or CTA.
- Source commentary: relying only on global duration fit and forgetting to check
  the actual frame where each named object appears.

# Edit Director - Avatar Spokesperson Pipeline

## When To Use

Turn the planned presenter scenes and produced assets into a coherent spokesperson timeline. The quality bar is steady delivery, readable support layers, and a clear CTA landing.

In `source_commentary` mode, this stage turns source footage, fitted narration,
captions, and optional avatar performance into a source-led short.

## Process

### 1. Cut The Presenter Track First

Assemble the core spokesperson performance before adding support layers. If the presenter cut is weak, extra graphics will not rescue it.

### 2. Add Support Layers Sparingly

Use overlays only where they help:

- short proof points,
- product names,
- pricing or feature cards,
- CTA reinforcement,
- subtitles.

### 3. Respect Spoken Rhythm

Keep pauses where they help emphasis. Do not trim so tightly that the avatar feels rushed or robotic.

### 4. Plan Deliverables Clearly

Recommended metadata keys:

- `hero_cut_order`
- `cta_frame_range`
- `overlay_timing_map`
- `variant_decisions`
- `source_audio_treatment`
- `avatar_layout_mode`
- `caption_timing_map`
- `beat_map_spot_checks`

### 5. Quality Gate

- the presenter remains the anchor,
- overlays are timed cleanly,
- scene transitions are calm and intentional,
- the CTA lands once and clearly.

## Source-Commentary Edit Rules

Choose one mode deliberately:

- `source_top_avatar_bottom`,
- `avatar_top_source_bottom`,
- `source_full_avatar_overlay` (circle facecam bubble),
- `source_full_avatar_cutout` (green-screen style: cut-out persona bottom-left over a large source),
- `voiceover_only`.

Layout geometry, cut-out method, and cost notes: `persona-avatar-production.md` §4.

### Retime Source To Voice

Once real voice timings exist (`artifacts/voice_lines.json`), move or extend
source segments so every named visual lands at or just before its line. Source
edits are free; audio/avatar regenerations are paid. Record the new cut list in
`edit_decisions.json -> hero_cut_order`.

### Edit Toolkit That Worked (2026-09-24)

- **Freeze + push-in** (2s, zoom 1.00→1.15) on the payoff frame, timed to the
  persona's biggest reaction line.
- **Punch-in zoom** (1.00→1.12 over the segment) on comedic beats (fall, crash).
- **Stat card** for verified numbers (e.g. `ROBOT 8.84s / BOLT 9.58s`), shown
  only while the number is spoken, never covering the action.
- **Captions** in 3-word chunks spread across each line's spoken span, no two
  chunks on screen at once; key words in yellow; digits in captions even when the
  voice spells them out (`caption_overrides`, `highlight_words`).
- End on a freeze of the funniest/most-shared moment, not on a black frame.

Set source audio treatment:

- mute,
- duck under narration,
- keep only key reaction moments,
- reject if original dialogue is essential.

Captions must be in line with the spread of the video:

- keep them readable on mobile,
- place them away from key bottles, hands, labels, score, prize, or faces,
- move caption zones when the source action changes,
- avoid covering the visual trigger while the narrator names it.

If the narration was speed-fitted, record the speed factor and confirm the beat
map still lines up after the fit.

## Common Pitfalls

- Overcutting to simulate energy.
- Letting captions, side panels, and lower thirds compete for the same area.
- Ending without a clean CTA hold.
- Source commentary: placing captions where they hide the exact action the
  narrator is telling viewers to watch.

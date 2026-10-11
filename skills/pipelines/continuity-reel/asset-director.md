# Asset Director — Continuity Reel Pipeline

## When to Use

You produce every asset for a fully-generated cinematic continuity reel: the canonical
entity images, the identity-conditioned derived views, the image-to-video motion clips,
ONE continuous narration take, and word-by-word captions. Identity, observable behavior, voice performance, and audible musical emotion
all contribute to the reel.

Read [Audio Direction](audio-direction.md) before making voice, music, or timing decisions.

Read [Visual Production and Review](visual-production-review.md) for reference mapping,
failed-take review, and evidence required before batching.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Records `visual_entity_id`, `entity_role`, `reference_path`, `continuity_score` |
| Prior | `scene_plan`, `visual_memory`, `script`, `research_brief.visual_references` | What to generate, in what order; real appearance and environment references |
| Guides | `creative/image-gen-usage.md`, `creative/prompting/kling-prompting.md`, `creative/video-gen-prompting.md` | Prompt construction |
| Tools | `flux_image` (canonical), `flux_kontext_image` / `image_selector` edit (derived), `kling_video` (i2v), `tts_selector` / `elevenlabs_tts` (narration), `lib/clip_embedder` (gate) | Generation |

## Process

### Step 1: Order generation CANONICAL-FIRST

Sort `scene_links` so every entity's `canonical_introduction` is generated before its
`derived_view`s. A derived view cannot be conditioned on a canonical that doesn't exist yet.

### Step 2: Generate each canonical (text-to-image, max quality)

Use `flux_image` from the entity's `identity_anchors` + the canonical scene's
`shot_language`. This is the most important image in the entire reel — a bad canonical
contaminates every derived view. Inspect/approve before proceeding. Bind the path back:
`visual_memory.<entity>.canonical_asset_path = <generated path>`, and pin
`generator_locked` so all views use the same model (no cross-provider style leak).

Before writing the canonical prompt, review `research_brief.visual_references` and extract
the subject's real appearance anchors:
- anatomy/proportions,
- color and markings,
- scale cues,
- habitat/environment cues,
- macro details that the audience would expect.

Reject anatomy errors before deriving more views. Inspect the details the script
will emphasize (bill, feet, limb count, scale) against the research. A visually
polished canonical can still be wrong. Also inspect focus, background brightness,
and habitat readability; avoid an indistinct color field when context matters.

The canonical prompt should reflect these facts. Do not invent a generic creature/product
when the research references show a specific shape or visual signature.

### Step 3: Generate derived views — STAR topology, identity-not-composition

For each `derived_view`, condition on the entity's **canonical** asset (never a previous
derived view). Use `flux_kontext_image` / `image_selector` edit mode with
`image_path = canonical_asset_path`.

**The prompt must request a NEW composition, not a copy.** Kontext editors will recreate
the reference frame if you tell them to "keep the same image." Instead:
> "Use the provided image as the identity and style reference ONLY, not the composition to
> copy. New shot: [the `reuse.variation` — new camera angle / pose / framing]."

Do NOT write "same plumage, same colors, same subject" as the whole prompt — that tells it
to copy and is why extreme reframes fail. Name the identity once via the reference, then
describe what CHANGES.

Also include the scene's `environment_role` / `environment_notes`. A good derived prompt
changes at least two of:
- shot size,
- camera angle,
- action state,
- background/habitat,
- viewer perspective,
- screen grammar (POV, split/composite, aftermath, insert).

The correct outcome is "same entity, new moment," not "same frame with a small prop added."

### Step 4: Continuity gate (verify identity held)

Use the registered/local continuity checker when available and record its measured
similarity against the canonical. Inspect anatomy, pose, props, and contact separately:
a high similarity score does not prove any of these are correct. Below-threshold takes
may be retried only within the remaining budget (at most two retries); preserve costs
and flag unresolved failures instead of declaring the best failed take a pass.

If the checker fails to load, record the failure and omit the numeric score. Do not
invent a score or claim automated acceptance. Manually inspect start/middle/end and
record specific observations. A human-requested review draft can proceed with explicit
warnings; it does not establish a production quality pass.

### Step 4b: Extreme-crop / macro derived views

If `reuse.variation` is a much tighter crop than the canonical (eye macro, talon close-up),
a prompt alone will NOT reframe enough — Kontext preserves composition. Instead:
1. **Crop the canonical** to the target region (the eye, the talons) with a center/region crop.
2. Use that crop as the `image_path` reference.
3. Prompt the detail/motion. This produces a true macro that still matches the canonical.

Do not jump more than ~2 shot-size steps with a pure prompt.

### Step 5: Motion — image-to-video for motion-led & hero beats

For scenes with `type: video` (and at minimum every `hero_moment`), generate real motion
with `kling_video`, `operation: image_to_video`, `image_path = the scene's approved still`,
the exact `model_variant` and duration locked in the production plan, and
`aspect_ratio: 9:16`. Inspect selector support for variant forwarding; do not let
a missing selector parameter silently select a different, more expensive model.

Follow `creative/prompting/kling-prompting.md`: **prompt MOTION, not appearance** (the still
already defines the look). One clear action + one camera behavior. Add `same subject, no
morphing`. Verify the current price for the exact endpoint before spending. Budget
generated seconds, not finished timeline seconds, and include samples, discarded
takes, retries, narration, and music. Reserve uncertain calls until reconciled;
a timeout is not evidence that a provider did not charge. Reuse accepted samples.

For reference-driven work, inspect the hardest causal action before the remaining
motion batch. Compare its start, middle, and result against the scene's behavior
contract; reject a plausible-looking subject that never performs the claimed action.

> fal storage upload (`rest.alpha.fal.ai/storage/upload`) rate-limits to HTTP 403 after a
> burst of ~10 uploads. Space i2v calls out or retry with backoff; do NOT silently downgrade
> a motion beat to a still zoom without flagging it.

### Step 6: Narration — ONE continuous take (not per-line)

Generate the ENTIRE script in one call through the approved registered TTS tool. Generating each
line separately produces cold-start, disjointed, "cluttering" audio — the single most common
narration failure. One call = one natural performance.
- Use natural punctuation and short breaths as a starting point. Derive pacing
  from the approved reference and measured performance; do not insert a fixed
  long pause between every beat or add silence merely to fill the video.
- Select and record the voice and supported settings using `audio-direction.md`.
- Prefer provider timestamps when the registered tool supports them. Otherwise
  transcribe the single generated take locally and verify alignment against the
  approved script. Never invent word timestamps or claim provider alignment was used.
- Parse word timestamps for caption timing. **Skip characters inside `<...>` break tags**
  when rebuilding words (the tag chars appear in the alignment stream).
- An explicitly selected voice or approved channel preference satisfies voice selection;
  apply the preview policy in `audio-direction.md` without redundant approval requests.

### Step 6b: Background music (every reel gets a score)

Use the approved library track or generate one instrumental bed through the approved
music tool. Follow `audio-direction.md` for emotional arc, prompt construction, and
voice pairing. Reuse a suitable existing track when its mix is the problem.
- Plan coverage from the measured narration plus tail. Document an extension or
  loop when needed and check its join in the rendered mix.
- Record the original track in the manifest. Measure its level; compose must select
  gain and ducking for this source instead of inheriting a fixed percentage.
- Verify current account/model pricing before generation, including retries.

### Step 6c: Ambience / noise-floor plan

Plan an ambience layer for the compose stage when the subject has a strong environment
or the narration contains audible pauses. This can be:
- a generated or sourced ambient bed (`sfx` / `audio` asset), or
- a local ffmpeg noise-floor texture created during compose (for example filtered brown
  noise for underwater, wind, cave rumble, room tone).

The ambience should sit below narration and music and serve the scene. A silence
detector is diagnostic; adding noise does not prove emotional engagement. Record generated/sourced ambience
assets in `asset_manifest`; local compose-generated ambience can be noted in `render_report`
and `edit_decisions.audio`.

### Step 7: Assembly discipline (learned failure modes)

- **Do NOT trim motion clips to narration length.** A 5s clip cut to a 1.6s narration line
  throws away motion and feels broken. Let each scene play its full clip (or sync the scene
  to the narration *window* = this beat's start → next beat's start), and let the caption
  HOLD after the last word while motion finishes.
- **Phrase captions:** follow the approved edit plan, replacing each phrase as speech
  advances. Never accumulate a paragraph. Burn via PNG overlays when needed.
- **Round xfade offsets** (`:.3f`) — unrounded floats error the xfade filter.
- One continuous narration track over the whole timeline carries flow even across hard cuts.

### Step 8: Build the asset manifest

Record per asset: `visual_entity_id`, `entity_role` (canonical|derived), `reference_path`,
measured `continuity_score` when available, `seed`, `model`, `cost_usd`.
Omit unsupported fields; document unavailable checks in metadata. Verify every path exists.

## Common Pitfalls

- **Re-describing the subject in derived/i2v prompts** → copy or morph. Reference = identity; prompt = the change.
- **Chaining derived→derived** → compounding drift. Always condition on the ONE canonical.
- **Repeating the same environment** → visual monotony. The entity stays consistent; the
  setting, POV, action, and screen grammar should change.
- **Per-line TTS** → disjointed narration. One continuous take.
- **Trimming clips to narration** → choppy, "cut short." Full clips / sync to beat windows.
- **Pure-prompt macros** → no reframe. Crop the canonical first.
- **Silent provider downgrade** (video→still, or model swap) after the user approved a path — stop and ask.

## Fork approval and repair policy

Read `docs/CONTINUITY_REEL_FORK.md`. Scene approval must precede samples; subject-reference and hardest-action sample approval must precede the remaining batch. Record the user decision in project artifacts. An initial attempt plus two failed repairs of an essential shot requires a stop and user decision, even if generic review guidance permits passing with warnings.

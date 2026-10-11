# Kling 2.6 Prompting Guide

> Source: fal.ai Kling 2.6 Pro Prompt Guide (https://fal.ai/learn/devs/kling-2-6-pro-prompt-guide)
> Tool: `kling_video` (provider `kling`, via fal.ai). Operations: `text_to_video`,
> `image_to_video`, `first_last_frame_to_video`.

## When to Use

When writing prompts for `kling_video` — OpenMontage's primary **image-to-video**
engine. Lock the approved endpoint/variant and verify its current price before spending;
example variants here are not a default or a price guarantee. Kling is useful for
turning an approved still into a controlled, identity-stable motion shot.

For the universal motion vocabulary (shot types, camera moves, lighting), see
`creative/video-gen-prompting.md`. This guide covers Kling-specific syntax and the
image-to-video discipline that matters most for OpenMontage reels.

## The 4-Part Structure (text-to-video)

Kling responds best to prompts organized in this order:

```
[Scene Setting]   environment + lighting, established first
[Subject]         the main subject with specific attributes
[Motion]          precise camera + subject movement directives
[Style]           aesthetic / grade / quality cues
```

Example:
```
A wet rainforest canopy in soft overcast light.
A harpy eagle with a grey-white facial disc and black crown feathers perched on a mossy branch.
The eagle slowly turns its head toward camera and blinks; leaves sway gently behind it; locked camera.
Cinematic wildlife documentary, shallow depth of field, photorealistic.
```

## Image-to-Video — the rule that matters most

**When an image is provided, the composition is ALREADY DECIDED. Prompt MOTION, not appearance.**
Do not re-describe what the subject looks like — the still defines that. Describe only
what *moves* and how the *camera* behaves.

- ✅ "The eagle turns its head and blinks; feathers ruffle in a light breeze; camera holds steady."
- ❌ "A harpy eagle with grey-white facial disc, black crown feathers, white belly, perched on a branch…" (re-describing the still — wastes the prompt and invites drift/morphing)

Keep i2v prompts **short and motion-focused**. One clear action + one camera behavior is
usually better than three. Complexity is the #1 cause of motion distortion.

### Observable behavior and contact

For a causal hero action, write the visible starting state, one action, and the
result that must persist: “The bird releases its bill and lifts its head; the cached
prey stays secured on the same thorn.” Keep the contact point visible and camera
movement restrained. A head turn is suitable atmosphere but cannot substitute for
a feeding, placement, or transformation claim. Inspect the start, action, and result
before batching. Reject an incorrect starting still; motion prompts do not repair
wrong anatomy, attachment geometry, or an implausible prop. Anti-morphing wording
is guidance to the model, not proof that the output passed.

### Identity stability (anti-morphing)

Kling can let a subject "morph" mid-clip. To hold identity:
- Add `maintains exact appearance throughout` or `same subject, no morphing`.
- Prefer **simple motion**. "360° rotation while zooming in" reliably warps geometry — avoid.
- For a recurring entity (see `visual_memory`), the still IS the identity anchor; the i2v
  prompt should never reintroduce conflicting descriptors.

## Emphasis Syntax

Kling supports `++…++` to prioritize an element:
```
++the eagle's wings spread wide++, launching toward camera, talons forward
```
Use it on the single most important action or subject — not on everything (that defeats it).

## Negative Prompting

State unwanted elements explicitly:
```
No people, no text, no logos, no morphing, no extra limbs, no warped anatomy.
```

## first_last_frame_to_video (continuity chains)

Kling can animate **between two approved keyframes** (`first_frame_path` + `last_frame_path`).
Use this when you have a canonical start and a target end pose from the same entity:
```
Animate smoothly from the first frame to the last frame as one continuous shot.
Keep the same subject identity, scale, anatomy, and palette. [camera behavior].
No morphing, no new subjects, no text.
```
Regenerate a bad keyframe BEFORE making the clip — Kling animates what it's given; it
will not fix a wrong subject.

## Motion & Camera Vocabulary (Kling-friendly)

- Camera: `stable/locked camera`, `smooth tracking`, `slow push-in`, `gradual pull back`,
  `tracks alongside`, `slow orbit` (gentle, not full 360°).
- Subject micro-motion (great for wildlife realism): `slow blink`, `head turn`,
  `feathers ruffle in a light breeze`, `subtle breathing`, `eyes dart`, `tail flicks`.
- Hero/action beats: `wings spread wide`, `lunges toward camera`, `leaps`, `takes flight`.

## What to Avoid

| Don't | Why | Do Instead |
|-------|-----|-----------|
| Re-describe the still in i2v | Wastes prompt, invites drift | Describe only motion + camera |
| "360° rotation + zoom" | Warps geometry | One simple camera move |
| Slow-motion + time-lapse together | Contradictory → unpredictable | Pick one temporal feel |
| Overloaded multi-action prompts | Motion distortion | One action + one camera behavior |
| Conflicting lighting terms | Breaks coherence | Keep the still's lighting; don't fight it |
| Readable text / logos | Not rendered reliably | Add text as overlay in compose |

## Example — OpenMontage i2v beat (from an approved canonical still)

```
operation: image_to_video
image_path: assets/eagle_canonical.png
prompt: |
  ++The harpy eagle slowly turns its head toward camera and blinks++;
  facial-disc feathers shift in a light breeze; locked camera, shallow depth of field.
  Same subject, no morphing.
duration: 5
model_variant: v3/standard
aspect_ratio: "9:16"
```

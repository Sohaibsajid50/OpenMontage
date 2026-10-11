# Scene Director — Continuity Reel Pipeline

## When to Use

You are the Scene Planner for a **fully AI-generated cinematic short** built around
**recurring visual entities** — the same animal/character/object returning across many
shots (e.g. the same harpy eagle from an eye macro to a full-wingspan launch). This is
NOT an explainer (no charts/diagrams) and NOT a source-footage cinematic piece (no real
clips). Every visual is generated, and **object-identity continuity is the whole point**.

This is where the script becomes a shot list AND a `visual_memory` declaration.

Read [Visual Production and Review](visual-production-review.md) for reference mapping,
failed-take review, and evidence required before batching.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Scene list + per-scene `visual_entity_id` / `reuse` |
| Schema | `schemas/artifacts/visual_memory.schema.json` | Entity registry you populate |
| Prior | `state.artifacts["script"]`, `state.artifacts["video_analysis_brief"]` (if reference-driven) | Beats + reference structure |
| Guides | `creative/image-gen-usage.md`, `creative/video-gen-prompting.md`, `creative/prompting/kling-prompting.md` | How the asset stage will prompt |

## Core Concept — Entities vs Scenes

A **visual entity** is a thing with a persistent identity (HARPY_EAGLE_01). A **scene**
is one shot of it. Many scenes can show one entity from different angles. Your job:

1. Identify the recurring entities in the script.
2. For each entity, pick ONE **canonical** scene that defines it (the clearest, most
   neutral hero view — usually a medium/wide front view, NOT an extreme crop).
3. Mark every other appearance as a **derived_view** that references the canonical.

## Process

### Step 0: Realize the selected hook mode

Make the first scene `narrative_role: "hook"`. Show the script's signature
behavior, consequence, anomaly, or transformation before an establishing scene,
neutral canonical, or identity portrait.

- For `spectacle_montage`, use multiple short phases only when each advances
  impact, scale, reaction, mechanism, or consequence.
- For `impossible_tableau`, use one coherent motion shot and hold it long enough
  to understand. Do not add decorative cuts to imitate another Reel.

In either mode, the first visual must match the spoken/on-screen claim. Record
`hook_mode`, `proof_visible_at_seconds`, and `identity_reveal_at_seconds` in scene
plan metadata.

For an animal behavior or transformation, also specify a visible causal sequence:
**setup → action → result/reaction**. Keep the subject, geography, and relevant
objects understandable across that sequence. This adapts Huobao's useful practice
of preserving a causal beat within a scene; it does not require that provider or
its fixed segment lengths.

Store `behavior_contracts` keyed by scene ID in scene-plan `metadata` (the scene
schema has no per-scene metadata field). For each hero beat record: the narration
claim, starting state, observable action, final state, and visual rejection
conditions. For example, a sea-snake impersonation requires the planned arm
arrangement to be readable; a generic octopus waving its arms is not sufficient.
Review the actual generated action against this contract before a full batch.
Identity similarity alone cannot establish correct anatomy or behavior. Generated
footage illustrates a sourced fact; it does not itself verify that fact.

### Step 1: Read the script and find entities

Carry the script's `metadata.claim_visual_map` into scene-plan
`metadata.claim_coverage`, keyed by section ID with the realizing scene IDs.
Multiple scenes may share `script_section_id`; show the setup, action, and result
where needed rather than forcing a cut at every sentence. Each scene's
`information_role` must name what new information it adds. A macro earns its
place by explaining a relevant detail, not merely by looking cinematic.

Write image prompts around subject/identity, pose, object geometry/contact,
framing and focus, then lighting/style. Describe motion separately as a limited
observable action with a persistent result. For derived views, distinguish what
identity must remain from what pose/composition must change. Do not replace
specific geometry with adjectives such as "powerful" or "dramatic".


For each beat, ask: *what is on screen, and have we seen it before?*
- New recurring thing → create a visual entity (`HARPY_EAGLE_01`, `PREY_MONKEY_01`).
- Same thing, new angle → derived_view of the existing entity.
- One-off background/environment → a `style_anchor` entity (carried by prompt, not by reference).

**Same-object vs same-concept (critical judgment):** Only chain identity when it is
literally the *same individual*. Two different neurons both "about neurons" are same-*concept*
(let them vary). The same neuron network returning in scene 7 is same-*object* (lock identity).
Forcing identity on same-concept shots makes the reel monotonous; missing it on same-object
shots breaks the illusion.

### Step 2: Choose the canonical view per entity

The canonical asset is the reference every derived view conditions on (star topology —
prevents drift). Pick a view that:
- shows the entity clearly and fairly neutrally (medium or wide, front or 3/4),
- contains the identity anchors (the traits that must persist),
- is NOT an extreme crop (you can't derive a wide shot from an eye macro).

Record in `visual_memory`:
```json
{
  "id": "HARPY_EAGLE_01", "kind": "generated", "reuse_topology": "canonical_anchor",
  "generator_locked": "flux_kontext", "canonical_scene_id": "scene-02-identity",
  "identity_anchors": ["grey-white facial disc","twin black crown feathers","amber eye","dark slate wings","white belly"],
  "allowed_variations": ["shot_size","camera_angle","wing_position"],
  "continuity_threshold": 0.83
}
```

### Step 3: Plan shot and environment variety per entity

A great reel shows ONE entity many ways. Across an entity's scenes, deliberately vary
`shot_language.shot_size` (extreme_close_up → wide), `camera_movement`, environment,
screen language, and viewer perspective. Mark the visual peak with `hero_moment: true`
(e.g. wings-spread launch).

Continuity does **not** mean repeating the same background. Keep the entity's identity
stable, but change the world around it. After the opening proof, plan a sequence
that includes several of these:
- Establishing environment shot (never automatically first).
- Identity/beauty shot.
- Macro detail or weapon/detail insert.
- Prey/object POV.
- Split-screen, composite, x-ray-style, or diagram-like cinematic insert.
- Impact/action shot.
- Aftermath or wide pullback.
- Final hero portrait.

Flag more than two consecutive beats with unchanged information or framing.
Keep location and framing stable when that makes a causal sequence easier to
understand; record the reason in `metadata.continuity_exceptions`. If the scene list starts to feel like "same animal, same burrow,
slightly different shell," revise before asset generation.

**Macro/extreme-crop scenes need a flag for the asset stage.** When a derived view is a
much tighter crop than the canonical (e.g. eye macro from a full-body canonical), Kontext
i2i will NOT reframe enough on its own. Set the `reuse.variation` explicitly to the crop
("extreme macro of the eye only") so the asset director knows to **crop the canonical to that
region before conditioning** (see asset-director Step 4b). Do not expect a pure prompt to
jump more than ~2 shot-size steps.

### Step 4: Write each scene (with continuity fields)

```json
{
  "id": "scene-05-eye", "type": "generated",
  "description": "Extreme macro of the eye, pupil sharp",
  "start_seconds": 12.0, "end_seconds": 15.5, "script_section_id": "vo-05",
  "narrative_role": "evidence", "hero_moment": true,
  "shot_language": { "shot_size": "extreme_close_up", "camera_movement": "dolly_in",
                     "lens_mm": 200, "lighting_key": "overcast_soft", "depth_of_field": "shallow" },
  "environment_role": "macro_detail_insert",
  "environment_notes": "background reduced to blurred feather texture; not the same branch setup as previous scene",
  "visual_entity_id": "HARPY_EAGLE_01",
  "reuse": { "role": "derived_view", "reference": "canonical", "variation": "extreme macro of the eye only" },
  "required_assets": [
    { "type": "image", "description": "macro eye, identity-conditioned on canonical", "source": "generate" }
  ]
}
```
- The canonical scene uses `"reuse": { "role": "canonical_introduction" }` and no `reference`.
- `type` is `generated` for stills and `video` for motion-led / hero beats (asset stage
  will route `video` to `kling_video` image_to_video conditioned on the canonical still).

### Step 4b: Narration timing (drives everything downstream)

Narration is generated as ONE continuous take (asset stage), so write beats that read as
a single performance. Budget **2.0–2.5 words/sec** as a starting point, then fit cadence
to the selected hook mode and available motion. Note per beat which visual entity is on
screen so the asset stage can align scenes to word timestamps. Longer pauses are valid
only when meaningful motion, music, captions, or a visual payoff continues carrying the
screen; never add dead air merely to feel cinematic.

### Step 5: Self-evaluate

| Criterion | Question |
|-----------|----------|
| Entity coverage | Does every recurring subject have a visual_memory entity + one canonical? |
| Same-object discipline | Did you chain identity ONLY where it's literally the same individual? |
| Shot variety | Does each entity appear in genuinely different shot sizes/angles? |
| Environment variety | Do consecutive scenes change location, POV, screen grammar, or action state? |
| Macro flags | Are extreme-crop derived views flagged so the asset stage crops the canonical? |
| Hero moment | Is the visual peak marked and given a motion (`video`) treatment? |
| Behavior first | Is scene 1 the signature behavior/consequence rather than context or portraiture? |
| Hook mode | Does opening shot duration and cut density fit the selected mode? |
| Claim sync | Does the opening image prove or concretely tease the exact hook line? |

## Common Pitfalls

- **Choosing an extreme crop as the canonical** — you can never derive wider shots from it. Canonical = neutral medium/wide.
- **Chaining derived→derived** — always reference the ONE canonical (star topology), never the previous derived view; chaining compounds drift.
- **Same-concept forced as same-object** — makes the reel feel like one looping shot.
- **Expecting Kontext to jump shot sizes** — flag macros for crop-conditioning instead.
- **Context before proof** — move habitat and neutral identity shots after the hook.
- **Portrait for an action claim** — eyes and beauty shots cannot prove a strike or transformation.
- **Universal pause timing** — let causality, motion, and audio determine cadence.
- **Mistaking continuity for repetition** — the same subject in the same environment for
  every beat feels static. Preserve identity; vary environment, shot grammar, and action.

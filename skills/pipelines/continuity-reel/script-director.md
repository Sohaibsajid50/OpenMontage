# Script Director — Continuity Reel Pipeline

## When to Use

You write the **narration script and opening hook** for a fully-generated
continuity reel about any subject — animal, person, place, event, discovery,
concept. The script you produce drives everything downstream: each beat becomes
one or more shots of a recurring visual entity. A boring or
encyclopedia-style script produces a boring reel no matter how good the visuals.

Read [Audio Direction](audio-direction.md) before making voice, music, or timing decisions.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Skill | `skills/creative/narrative-hook-engine.md` | The hook + retention-arc method (READ IT FIRST) |
| Schema | `schemas/artifacts/script.schema.json` | Script artifact validation |
| Prior | `proposal_packet`, `video_analysis_brief` (if reference-driven) | Subject, target duration, approved direction |
| Tools | `web_search` | Research the subject for the evidence packet (never invent facts) |

## Process

### Step 1 — Read the hook engine and build the evidence packet
Read `skills/creative/narrative-hook-engine.md`. Research the subject (web search
if you lack the facts) and fill the **Subject Evidence Packet** (Step 1 there).
If a field is unknown, mark it `unknown` — do not fabricate.

### Step 1b — Choose an explainable story before polishing the hook
For a mechanism-led reel, write one sentence identifying the viewer's question and
one sentence answering it. Build the body around the constraint, action, and
consequence needed to understand that answer. A biography or event may need a
different arc; do not force every subject into the shrike's anatomy/food pattern.

For reference-led work, read the observed transcript and shot map: identify what
is visible, what the viewer knows, and what remains unresolved at each beat.
Transfer those narrative functions, not unsupported claims or incidental imagery.
For an approved recreation, preserve the selected hook/direction; do not reopen
concept selection merely to fill a hook lab.

Check relevant prior project evidence when available. Match the script version to
the render being reviewed. A saved plan, self-score, technical pass, and user
preference are different evidence; none establishes audience retention or virality.

### Step 2 — Run the Hook Lab
For an open concept, explore distinct hook/visual pairs using the hook engine.
For an already approved hook, audit its truth, visible promise, and payoff instead
of generating replacement candidates. Score with the weighted rubric, apply the
hard gates, and select the winner. Classify every finalist as
`spectacle_montage` or `impossible_tableau`; choose the mode from the available
behavior and footage, not personal preference. Record the full hook lab.

### Step 3 — Write the full retention arc
Use the engine's arc as a starting point: **hook → stakes → escalation →
turn/reveal → landing**. Every beat answers the prior question and opens the next
(loop discipline). Answer beats need not introduce another artificial mystery. One idea per beat. Documentary pacing 2.0–2.5 words/sec with
short breaths — not long pauses.

### Step 4 — Fit duration and handoff to scenes
- Target the duration from the proposal (typically 30–60s).
- Each `section` is a narration beat. Several shots may share its
  `script_section_id` when the explanation needs setup, action, and result. Write beats the scene-director can map to
  a clear recurring subject (so continuity has something to lock onto).
- The first section's `text` MUST be the selected hook, with `beat_role: "hook"`.
- The first beat starts at 0.0s unless an approved `spectacle_montage` uses a
  visual cold open. Nothing informational may precede it.
- Put the selected hook mode and opening visual pair in metadata. The visual must
  show the claimed behavior/consequence now; a line about a punch over eyes,
  habitat, or a neutral portrait fails.
- Reveal identity and habitat only after the behavior hook.
- For reels longer than 20s, include a `re_hook` around 8–12s.

Store a `metadata.claim_visual_map` keyed by section ID. For each beat record:
- `claim` and a source reference (with uncertainty retained in the spoken wording);
- `viewer_question`, `answer_added`, and the intended payoff connection;
- `visible_evidence`: what the generated illustration must actually show;
- `generation_risk` and a concrete `reject_if` condition for its essential visual.
A portrait can introduce identity; it cannot demonstrate hunting. Wing blur can
suggest speed; it cannot demonstrate a precise wing path. Avoid promising a
transformation with only before/after portraits unless that treatment is explicit.

Identify the hardest indispensable shot before generation. If its plan is not
credible within the approved motion path and budget, revise the promise/treatment
before committing to all assets. Planned feasibility is not an observed pass.

### Step 5 — Self-evaluate
| Criterion | Question |
|-----------|----------|
| Hook strength | Does beat 1 open a real curiosity gap from a true fact, not a template? |
| Verbal/visual pair | Does the hook's opening shot work as a still and match the line? |
| Behavior first | Does signature behavior/consequence precede identity and context? |
| Mode fit | Does the hook use montage or tableau grammar for a concrete reason? |
| Re-hook | For a reel over 20s, does a fresh question or complication arrive around 8–12s? |
| Loop chain | Does every beat answer one question and raise the next? |
| Visual feasibility | Does each essential claim have a readable planned illustration and a rejection condition? |
| Explanation | Does the middle explain the hook instead of accumulating impressive facts? |
| Truth | Is every claim grounded in the evidence packet (no fabrication)? |
| Payoff | Does the turn/reveal deliver what the hook promised? |
| Pacing | 2.0–2.5 words/sec, one idea per beat, short breaths? |
| Landing | Does the final beat resonate rather than trail off? |

If any criterion is weak, revise before submitting.

### Step 6 — Submit
Emit the script artifact (schema-valid `script`) plus the hook lab in metadata.
Record `hook_mode`, `selected_hook_visual`, `behavior_visible_at_seconds`, and
`identity_reveal_at_seconds`. Each section carries `id`, `text`, timings, and
`beat_role`.

## Common Pitfalls

- **Encyclopedia opener** — "The X is a species of…" Lead with the most arresting
  true fact (use the Superlative / Information-gap / Counterintuitive families).
- **Fact dump** — three facts in one breath. One idea per beat.
- **Answering the hook** — stating the full payoff in beat 1 kills the reason to stay.
- **Flat body** — a strong hook then a list of facts. Keep opening loops through the middle.
- **No recurring subject** — beats that never return to one entity give the
  continuity system nothing to lock; keep a clear protagonist subject across beats.
- **Dead-air pacing** — writing for long pauses; the reel reads as "in steps."

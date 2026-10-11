# Visual Production and Review — Continuity Reel

Use with scene, asset, and compose direction. Record what was requested, what the
output actually shows, and what was accepted. A successful API response is not a
successful creative result. Save failed retries and unresolved visual limitations
in the current project’s review artifacts.

## Ground the reference in observed footage

For reference-driven work, produce a shot map from sampled frames, action intervals,
and transcript. Record the claim, shot size, subject/prop positions, contact point,
action/result, camera movement, focus/background, caption position, and purpose of
each shot. Unknown analyzer motion labels are unknown, not evidence of still footage.
Sample more densely around the mechanism than around an establishing view.

Separate the reference's narrative structure from its exact wording and branding.
Verify biological claims independently. A generated shot illustrates a claim; it
cannot establish the underlying fact or identify the source creator's tools.

## Make prompt revisions explicit and review their limits

Use this image prompt structure, adapted to the scene:

> Reference = subject identity/style only. New composition = [shot size, angle,
> framing]. Starting pose = [visible body arrangement]. Prop/contact = [what holds
> what, where, relative size]. Environment = [readable habitat and depth of field].

When a model copies the canonical pose, explicitly release composition and specify
the new arrangement. “In the beak, above the feet” is more actionable than repeating
“holding prey.” Keep the important contact visible rather than hiding the whole
mechanism. Anatomical dimensions and believable prop scale still require inspection.

Do not treat stronger adjectives, uppercase words, or longer prompts as reliable
fixes. “Long rigid wooden thorn” produced an oversized stake in the shrike retry.
Change the failed relationship or starting frame, then check for new failure modes.
Record seed changes too: changing both seed and text is not a controlled prompt test.

For macros, crop the relevant region of an approved canonical before requesting a
new view. This can help framing, but also magnifies bad anatomy. Never infer correct
bill/feet geometry merely because the crop or image has the right filename.

## Prove action before scaling production

Inspect the hardest motion at its setup, action, release/contact transition, and
result. The result must remain readable after contact changes. “Small head movement”
is acceptable atmosphere but cannot prove a placement or feeding mechanism.

Use `pass`, `partial`, or `reject` with observations and frame paths. If inspection
later contradicts an earlier pass, amend the durable review and halt dependent
batching until the action is resolved or explicitly accepted as a review-draft
limitation. Do not quietly lower the requirement to fit a pleasant-looking clip.

Retry only within the agreed budget. Reuse an existing approved frame when it still
serves the beat, and record the actual reference file plus the cost in shot variety.
If two scene attempts fail, say so; reusing another frame is not a successful new
composition. Record intent, observed result, rejection reason, selected take, and
remaining limitation in project metadata or a linked review artifact.

## Review the assembled picture, not just source clips

- Check that the cut preserves the action/result; trimming a valid source can remove
  the proof. If the window is too short, reconsider the edit instead of hiding it.
- Check the exact early frames for subject focus and motion blur. Separately review
  background brightness, color, depth, and habitat detail. Shallow depth of field is
  a deliberate choice, not an automatic synonym for cinematic quality.
- Include enough distinct shot scales and new information to justify cuts. A wide
  frame should reveal habitat or context, not just shrink the same portrait.
- Probe actual media dimensions and fps. A requested 9:16 output may arrive at a
  different ratio; record scaling/cropping and ensure it does not hide contact or
  captions. Upscaling does not create native high-resolution detail.
- Verify motion over time, separate audio/video duration, and actual ending frames.
  Report generated clips, completed edits, and remaining work distinctly. Give the
  user a playable artifact at the requested review milestone.

Keep claims and evidence separate across context resets. Preserve exact requests,
results, selected references, costs, and artifact versions. On resume, reconstruct
state from these files and relevant tool history; do not turn an earlier confident
commentary message into evidence that a quality check passed.

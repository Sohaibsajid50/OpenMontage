# Source Media Review Director - Avatar Spokesperson Source Commentary

## When To Use

Use this stage to inspect the approved source locally and create the visual map
that the script must obey.

## Process

1. Download or ingest the selected video into the project workspace.
2. Probe duration, resolution, frame rate, and audio levels.
3. Extract frames across the full timeline, usually 1 frame per second.
4. Build contact sheets for the full video and any suspicious timing ranges.
5. Identify visual beats:
   - game setup,
   - rule reveal,
   - key attempts,
   - object appearances,
   - reversals,
   - final result.
6. For every named object/action likely to appear in narration, record the first
   timestamp where it is visible.

## Pre-Split Sources

Many viral explainers are already split-screen (B-roll on top, the creator
talking below, burned captions between). Before planning a layout:

1. Sample 4–5 full frames across the timeline.
2. Find the split row from the row-mean luminance jump (e.g. y=592 of 1080).
3. Crop only the B-roll region (e.g. 608x540 at y=0) and verify the crop at those frames.
4. Record ranges where the creator fills the whole frame as `unusable_ranges`
   in the beat map, and never cut to them.

## Beat Map Contract

Each beat should include:

```json
{
  "start": 35.5,
  "end": 42.0,
  "visual_trigger_time": 36.0,
  "description": "Coke bottle is first clearly visible",
  "frame_refs": ["assets/frames/second/frame_037.jpg"]
}
```

## Output

Write `source_media_review` and `beat_map`. Record frame paths, contact sheet
paths, media probes, audio treatment recommendation, and any ambiguity.

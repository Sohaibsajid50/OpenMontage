"""Render the green-screen-style overlay: race large behind, cut-out Mason popping up bottom-left.

Mason's cut-out comes from Apple Vision person masks (tools_local/person_mask.swift) applied
to the Kling avatar frames in renders/work/cut/{frames,masks}. Reuses captions/card from render_split.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

import render_split as base

CANVAS_W, CANVAS_H = 1080, 1920
RACE_W, RACE_H, RACE_Y = 1350, 1200, 170
CUT_DIR = base.WORK / "cut"
PERSON_CROP = tuple(base.EDIT.get("cutout", {}).get("person_crop", (200, 0, 560, 536)))  # x, y, w, h in half-size cut frames
MASON_W = 640
MASON_X = -30
CAPTION_CENTER_Y = 1290
CARD_CENTER_Y = RACE_Y + 150
OUTPUT = base.PROJECT / "renders/final_cutout.mp4"


def main() -> None:
    top = base.WORK / "top_pane.mp4"
    if not top.exists():
        top = base.build_top_pane()
    duration = base.EDIT["canvas"]["duration"]
    fps = base.EDIT["canvas"]["fps"]
    crop_x, crop_y, crop_w, crop_h = PERSON_CROP
    mason_h = int(round(crop_h * MASON_W / crop_w / 2) * 2)
    mason_y = CANVAS_H - mason_h

    inputs = ["-i", str(top),
              "-framerate", "30", "-i", str(CUT_DIR / "frames/f_%04d.png"),
              "-framerate", "30", "-i", str(CUT_DIR / "masks/f_%04d.png"),
              "-i", str(base.VOICE_TRACK)]
    input_count = 4
    overlays = []
    (base.WORK / "captions").mkdir(parents=True, exist_ok=True)
    for index, cue in enumerate(base.build_caption_cues()):
        png = base.WORK / "captions" / f"ccap_{index:02d}.png"
        width, height = base.draw_text_card(base.caption_parts(cue["text"]), base.EDIT["caption_style"]["size"], png)
        inputs += ["-i", str(png)]
        overlays.append((input_count, (CANVAS_W - width) // 2, CAPTION_CENTER_Y - height // 2,
                         cue["start"], cue["end"]))
        input_count += 1
    card_png = base.WORK / "captions" / "card_00.png"
    card = base.EDIT["overlays"][0]
    card_w, card_h = Image.open(card_png).size
    inputs += ["-i", str(card_png)]
    overlays.append((input_count, (CANVAS_W - card_w) // 2, CARD_CENTER_Y - card_h // 2,
                     card["start"], card["end"]))

    graph = [
        "[0:v]split=2[race][bgsrc]",
        f"[bgsrc]scale=-2:{CANVAS_H},crop={CANVAS_W}:{CANVAS_H},boxblur=30:3,eq=brightness=-0.2:saturation=0.8[bg]",
        f"[race]scale={RACE_W}:{RACE_H}:flags=lanczos,crop={CANVAS_W}:{RACE_H}[racebig]",
        f"[bg][racebig]overlay=x=0:y={RACE_Y}[stage]",
        f"[1:v]format=rgba,crop={crop_w}:{crop_h}:{crop_x}:{crop_y}[person]",
        f"[2:v]format=gray,crop={crop_w}:{crop_h}:{crop_x}:{crop_y},boxblur=1:1[alpha]",
        f"[person][alpha]alphamerge,scale={MASON_W}:{mason_h}:flags=lanczos,fps={fps},"
        f"trim=0:{duration},setpts=PTS-STARTPTS[mason]",
        f"[stage][mason]overlay=x={MASON_X}:y={mason_y}[c0]",
    ]
    last = "c0"
    for step, (stream, x, y, start, end) in enumerate(overlays):
        label = f"c{step + 1}"
        graph.append(f"[{last}][{stream}:v]overlay=x={x}:y={y}:enable='between(t,{start},{end})'[{label}]")
        last = label
    graph.append(f"[3:a]aresample=48000,aformat=channel_layouts=stereo,"
                 f"loudnorm=I={base.EDIT['mix']['loudness_target_lufs']}:TP=-1.5:LRA=11[mix]")
    base.run_ffmpeg([*inputs, "-filter_complex", ";".join(graph), "-map", f"[{last}]", "-map", "[mix]",
                     "-t", str(duration), "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p",
                     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(OUTPUT)])
    print(OUTPUT)


if __name__ == "__main__":
    main()

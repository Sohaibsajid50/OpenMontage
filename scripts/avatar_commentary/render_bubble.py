"""Render the source_full_avatar_overlay variant: race centered on a blurred fill, Mason in a round bubble.

Reuses the top pane, captions and stat card from render_split.py (same edit_decisions / voice_lines).
Usage: python render_bubble.py [avatar_video] [output]
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

import render_split as base

CANVAS_W, CANVAS_H = 1080, 1920
RACE_Y = 330
BUBBLE_DIAMETER = 440
BUBBLE_X, BUBBLE_Y = 40, 1430
RING_WIDTH = 8
CAPTION_CENTER_Y = 1350
CARD_CENTER_Y = RACE_Y + 130
FACE_SQUARE = tuple(base.EDIT.get("bubble", {}).get("face_square", (572, 20, 760)))  # x, y, side in the avatar frame


def make_bubble_masks(work: Path) -> tuple[Path, Path]:
    """Circle alpha mask for Mason plus a white ring with soft shadow."""
    scale = 4
    size = BUBBLE_DIAMETER * scale
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    mask_path = work / "bubble_mask.png"
    mask.resize((BUBBLE_DIAMETER, BUBBLE_DIAMETER), Image.LANCZOS).save(mask_path)

    pad = 30
    ring_size = BUBBLE_DIAMETER + 2 * pad
    shadow = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((pad, pad + 8, pad + BUBBLE_DIAMETER, pad + 8 + BUBBLE_DIAMETER), fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    ring = Image.new("RGBA", (ring_size * scale, ring_size * scale), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse(
        (pad * scale, pad * scale, (pad + BUBBLE_DIAMETER) * scale - 1, (pad + BUBBLE_DIAMETER) * scale - 1),
        outline=(255, 255, 255, 255), width=RING_WIDTH * scale)
    shadow.alpha_composite(ring.resize((ring_size, ring_size), Image.LANCZOS))
    ring_path = work / "bubble_ring.png"
    shadow.save(ring_path)
    return mask_path, ring_path


def main() -> None:
    avatar = Path(sys.argv[1]) if len(sys.argv) > 1 else base.PROJECT / "assets/video/mason_kling_avatar.mp4"
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else base.PROJECT / "renders/final_bubble.mp4"
    work = base.WORK
    work.mkdir(parents=True, exist_ok=True)
    top = work / "top_pane.mp4"
    if not top.exists():
        top = base.build_top_pane()
    mask_path, ring_path = make_bubble_masks(work)
    duration = base.EDIT["canvas"]["duration"]
    fps = base.EDIT["canvas"]["fps"]
    face_x, face_y, face_side = FACE_SQUARE

    inputs = ["-i", str(top), "-i", str(avatar), "-i", str(base.VOICE_TRACK),
              "-loop", "1", "-i", str(mask_path), "-loop", "1", "-i", str(ring_path)]
    overlays = []
    (work / "captions").mkdir(parents=True, exist_ok=True)
    for index, cue in enumerate(base.build_caption_cues()):
        png = work / "captions" / f"bcap_{index:02d}.png"
        width, height = base.draw_text_card(base.caption_parts(cue["text"]), base.EDIT["caption_style"]["size"], png)
        inputs += ["-i", str(png)]
        overlays.append((len(inputs) // 2 - 2, (CANVAS_W - width) // 2, CAPTION_CENTER_Y - height // 2,
                         cue["start"], cue["end"]))
    card_png = work / "captions" / "card_00.png"
    if card_png.exists():
        card = base.EDIT["overlays"][0]
        card_w, card_h = Image.open(card_png).size
        inputs += ["-i", str(card_png)]
        overlays.append((len(inputs) // 2 - 2, (CANVAS_W - card_w) // 2, CARD_CENTER_Y - card_h // 2,
                         card["start"], card["end"]))

    graph = [
        "[0:v]split=2[race][bgsrc]",
        f"[bgsrc]scale=-2:{CANVAS_H},crop={CANVAS_W}:{CANVAS_H},boxblur=30:3,eq=brightness=-0.18:saturation=0.8[bg]",
        f"[bg][race]overlay=x=0:y={RACE_Y}[stage]",
        f"[1:v]crop={face_side}:{face_side}:{face_x}:{face_y},scale={BUBBLE_DIAMETER}:{BUBBLE_DIAMETER},"
        f"fps={fps},format=rgba,trim=0:{duration},setpts=PTS-STARTPTS[face]",
        "[3:v]format=gray[mask]",
        "[face][mask]alphamerge[bubble]",
        f"[stage][4:v]overlay=x={BUBBLE_X - 30}:y={BUBBLE_Y - 30}:shortest=1[ringed]",
        f"[ringed][bubble]overlay=x={BUBBLE_X}:y={BUBBLE_Y}[b0]",
    ]
    last = "b0"
    for step, (stream, x, y, start, end) in enumerate(overlays):
        label = f"b{step + 1}"
        graph.append(f"[{last}][{stream}:v]overlay=x={x}:y={y}:enable='between(t,{start},{end})'[{label}]")
        last = label
    graph.append(f"[2:a]aresample=48000,aformat=channel_layouts=stereo,"
                 f"loudnorm=I={base.EDIT['mix']['loudness_target_lufs']}:TP=-1.5:LRA=11[mix]")
    base.run_ffmpeg([*inputs, "-filter_complex", ";".join(graph), "-map", f"[{last}]", "-map", "[mix]",
                     "-t", str(duration), "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p",
                     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(output)])
    print(output)


if __name__ == "__main__":
    main()

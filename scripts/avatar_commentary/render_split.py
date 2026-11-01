"""Render the source_top_avatar_bottom hero cut from artifacts/edit_decisions.json.

Top pane: source segments (optional push-in zoom) + freeze. Bottom pane: Mason avatar video.
Captions: PNG cards from artifacts/voice_lines.json (this ffmpeg has no drawtext/libass).
Audio: Mason's voice track only when the source is muted; loudness-normalized.

Usage: AVATAR_PROJECT=projects/<name> python scripts/avatar_commentary/render_split.py
Project-specific caption tweaks live in edit_decisions.json -> caption_style.caption_overrides / highlight_words.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(os.environ.get("AVATAR_PROJECT", Path.cwd())).resolve()
EDIT = json.loads((PROJECT / "artifacts/edit_decisions.json").read_text())
LINES = json.loads((PROJECT / "artifacts/voice_lines.json").read_text())
VOICE_TRACK = PROJECT / "assets/audio/mason_voice_track.wav"
WORK = PROJECT / "renders/work"
OUTPUT = PROJECT / "renders/final.mp4"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
CAPTION_MAX_WIDTH = 1000
WORDS_PER_CHUNK = 3
CAPTION_TEXT = EDIT["caption_style"].get("caption_overrides", {})
HIGHLIGHT_WORDS = set(EDIT["caption_style"].get("highlight_words", []))


def run_ffmpeg(args: list[str]) -> None:
    """Run ffmpeg quietly and fail loudly."""
    result = subprocess.run(["ffmpeg", "-v", "error", "-y", *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"ffmpeg failed: {result.stderr[-2000:]}")


def probe_size(path: Path) -> tuple[int, int]:
    """Return (width, height) of a video's first stream."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    width, height = out.strip().split(",")
    return int(width), int(height)


def draw_text_card(parts: list[tuple[str, bool]], size: int, path: Path) -> tuple[int, int]:
    """Draw stroked caption text; highlighted parts use the highlight color."""
    style = EDIT["caption_style"]
    font = ImageFont.truetype(FONT_PATH, size)
    stroke = style["stroke_width"]
    widths = [font.getbbox(chunk, stroke_width=stroke)[2] for chunk, _ in parts]
    width, height = sum(widths) + 2 * stroke, size + 4 * stroke
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    cursor = stroke
    for (chunk, highlighted), chunk_width in zip(parts, widths):
        fill = style["highlight"] if highlighted else style["fill"]
        draw.text((cursor, stroke), chunk, font=font, fill=fill, stroke_width=stroke, stroke_fill=style["stroke"])
        cursor += chunk_width
    if width > CAPTION_MAX_WIDTH:
        image = image.resize((CAPTION_MAX_WIDTH, int(height * CAPTION_MAX_WIDTH / width)), Image.LANCZOS)
    image.save(path)
    return image.size


def build_caption_cues() -> list[dict]:
    """Split each voice line into short chunks spread across its spoken span by character count."""
    cues = []
    for line in LINES:
        text = CAPTION_TEXT.get(line["id"], line["text"].upper().replace(",", ""))
        words = text.split()
        chunks = [" ".join(words[i:i + WORDS_PER_CHUNK]) for i in range(0, len(words), WORDS_PER_CHUNK)]
        total_chars = sum(len(c) for c in chunks)
        cursor = line["start"]
        for chunk in chunks:
            span = (line["end"] - line["start"]) * len(chunk) / total_chars
            cues.append({"text": chunk, "start": round(cursor, 2), "end": round(cursor + span + 0.12, 2)})
            cursor += span
    for current, following in zip(cues, cues[1:]):
        current["end"] = min(current["end"], following["start"])
    return cues


def caption_parts(text: str) -> list[tuple[str, bool]]:
    """Explicit *marks* win; otherwise highlight known key words."""
    if "*" in text:
        return [(c, i % 2 == 1) for i, c in enumerate(text.split("*")) if c]
    words = text.split()
    return [(w + (" " if i < len(words) - 1 else ""), w in HIGHLIGHT_WORDS) for i, w in enumerate(words)]


def zoom_filter(zoom: list[float] | None, frames: int, width: int, height: int, fps: int) -> str:
    """Centered push-in over the segment, or nothing."""
    if not zoom:
        return ""
    step = (zoom[1] - zoom[0]) / max(frames, 1)
    return (f",scale={width * 2}:{height * 2},zoompan=z='{zoom[0]}+on*{step:.6f}':x='iw/2-(iw/zoom/2)'"
            f":y='ih/2-(ih/zoom/2)':d=1:s={width}x{height}:fps={fps}")


def build_top_pane() -> Path:
    """Cut, crop, zoom and freeze the source into the top pane (video only)."""
    pane_w, pane_h = EDIT["top_pane"]["rect"][2:]
    crop_w, crop_h = EDIT["top_pane"]["source_crop"]
    crop_y = EDIT["top_pane"]["source_crop_y"]
    fps = EDIT["canvas"]["fps"]
    source = PROJECT / EDIT["source"]
    parts = []
    for seg in EDIT["hero_cut_order"]:
        part = WORK / f"seg_{seg['seg']}.mp4"
        duration = round(seg["out"][1] - seg["out"][0], 3)
        frames = int(round(duration * fps))
        base = f"crop={crop_w}:{crop_h}:0:{crop_y},scale={pane_w}:{pane_h}:flags=lanczos,setsar=1"
        if "freeze_src" in seg:
            still = WORK / f"freeze_{seg['seg']}.png"
            run_ffmpeg(["-ss", str(seg["freeze_src"]), "-i", str(source), "-frames:v", "1", "-vf", base, str(still)])
            run_ffmpeg(["-loop", "1", "-i", str(still), "-vf",
                        f"fps={fps}{zoom_filter(seg.get('zoom'), frames, pane_w, pane_h, fps)},setsar=1",
                        "-t", str(duration), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(part)])
        else:
            start, end = seg["src"]
            run_ffmpeg(["-ss", str(start), "-to", str(end), "-i", str(source), "-an", "-vf",
                        f"{base},fps={fps}{zoom_filter(seg.get('zoom'), frames, pane_w, pane_h, fps)},setsar=1",
                        "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(part)])
        parts.append(part)
    concat_list = WORK / "top_concat.txt"
    concat_list.write_text("".join(f"file '{p}'\n" for p in parts))
    top = WORK / "top_pane.mp4"
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(concat_list), "-c:v", "libx264", "-crf", "16",
                "-pix_fmt", "yuv420p", str(top)])
    return top


def build_final(top: Path) -> list[dict]:
    """Stack panes, overlay captions and cards, lay Mason's voice, encode."""
    canvas, bottom, divider = EDIT["canvas"], EDIT["bottom_pane"], EDIT["divider"]
    pane_w, pane_h = bottom["rect"][2:]
    mason = PROJECT / bottom["asset"]
    src_w, src_h = probe_size(mason)
    scale = max(pane_w / src_w, pane_h / src_h)
    scaled_w, scaled_h = int(round(src_w * scale / 2) * 2), int(round(src_h * scale / 2) * 2)
    (WORK / "captions").mkdir(parents=True, exist_ok=True)

    inputs = ["-i", str(top), "-i", str(mason), "-i", str(VOICE_TRACK)]
    overlays = []
    cues = build_caption_cues()
    for index, cue in enumerate(cues):
        png = WORK / "captions" / f"cap_{index:02d}.png"
        width, height = draw_text_card(caption_parts(cue["text"]), EDIT["caption_style"]["size"], png)
        inputs += ["-i", str(png)]
        overlays.append((len(inputs) // 2 - 1, (canvas["width"] - width) // 2,
                         EDIT["caption_style"]["center_y"] - height // 2, cue["start"], cue["end"]))
    for index, card in enumerate(EDIT.get("overlays", [])):
        png = WORK / "captions" / f"card_{index:02d}.png"
        line_pngs = []
        for line_index, line in enumerate(card["lines"]):
            line_png = WORK / "captions" / f"card_{index:02d}_{line_index}.png"
            draw_text_card([(line, line_index == 0)], 76, line_png)
            line_pngs.append(Image.open(line_png))
        card_w = max(im.width for im in line_pngs) + 60
        card_h = sum(im.height for im in line_pngs) + 50
        card_image = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 170))
        cursor = 25
        for im in line_pngs:
            card_image.alpha_composite(im, ((card_w - im.width) // 2, cursor))
            cursor += im.height
        card_image.save(png)
        inputs += ["-i", str(png)]
        overlays.append((len(inputs) // 2 - 1, (canvas["width"] - card_w) // 2,
                         card["center_y"] - card_h // 2, card["start"], card["end"]))

    graph = [
        "[0:v]setpts=PTS-STARTPTS[top]",
        f"[1:v]scale={scaled_w}:{scaled_h}:flags=lanczos,fps={canvas['fps']},"
        f"crop={pane_w}:{pane_h}:(iw-{pane_w})/2:(ih-{pane_h})/2,setsar=1,trim=0:{canvas['duration']},"
        "setpts=PTS-STARTPTS[bot]",
        f"[top][bot]vstack=inputs=2,drawbox=x=0:y={divider['y']}:w={canvas['width']}:h={divider['height']}"
        f":color={divider['color']}:t=fill[base0]",
    ]
    last = "base0"
    for step, (stream, x, y, start, end) in enumerate(overlays):
        label = f"base{step + 1}"
        graph.append(f"[{last}][{stream}:v]overlay=x={x}:y={y}:enable='between(t,{start},{end})'[{label}]")
        last = label
    graph.append(f"[2:a]aresample=48000,aformat=channel_layouts=stereo,"
                 f"loudnorm=I={EDIT['mix']['loudness_target_lufs']}:TP=-1.5:LRA=11[mix]")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    run_ffmpeg([*inputs, "-filter_complex", ";".join(graph), "-map", f"[{last}]", "-map", "[mix]",
                "-t", str(canvas["duration"]), "-c:v", "libx264", "-crf", "18", "-preset", "slow",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                "-movflags", "+faststart", str(OUTPUT)])
    return cues


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    top = build_top_pane()
    cues = build_final(top)
    (PROJECT / "artifacts/caption_cues.json").write_text(json.dumps(cues, indent=1))
    print(OUTPUT)


if __name__ == "__main__":
    main()

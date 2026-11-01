#!/usr/bin/env bash
# Cut the persona out of an avatar video locally (Apple Vision, no model download, macOS only).
# Usage: scripts/avatar_commentary/cut_person.sh <project_dir> <avatar_video>
# Writes <project_dir>/renders/work/cut/{frames,masks}/f_%04d.png for render_cutout.py.
set -euo pipefail

PROJECT_DIR="$1"
AVATAR_VIDEO="$2"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CUT_DIR="$PROJECT_DIR/renders/work/cut"
BINARY="$SCRIPT_DIR/.build/person_mask"

mkdir -p "$CUT_DIR/frames" "$SCRIPT_DIR/.build"
rm -f "$CUT_DIR"/frames/*.png "$CUT_DIR"/masks/*.png 2>/dev/null || true

if [ ! -x "$BINARY" ] || [ "$SCRIPT_DIR/person_mask.swift" -nt "$BINARY" ]; then
  swiftc -O "$SCRIPT_DIR/person_mask.swift" -o "$BINARY"
fi

# Half-size frames keep segmentation fast; the renderer scales the cut-out anyway.
ffmpeg -v error -y -i "$AVATAR_VIDEO" -vf "scale=iw/2:-2" "$CUT_DIR/frames/f_%04d.png"
"$BINARY" "$CUT_DIR/frames" "$CUT_DIR/masks"

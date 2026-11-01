"""Photo-to-talking-head video generation tool.

Animates a still face photo to appear as if speaking provided audio.
Hosted: Kling AI Avatar v2 Pro or sync-3 image-to-video on fal.ai (needs FAL_KEY).
Local: SadTalker or MuseTalk (needs a GPU install).
"""

from __future__ import annotations

import glob
import os
import shutil
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)
from tools.avatar._fal_avatar import FAL_AVATAR_ENDPOINTS, FAL_AVATAR_USD_PER_SECOND, run_fal_avatar
from tools.avatar._fal_queue import get_fal_api_key


class TalkingHead(BaseTool):
    name = "talking_head"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "avatar"
    provider = "sadtalker"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.HYBRID

    dependencies = []  # checked dynamically via get_status()
    install_instructions = (
        "Hosted: set FAL_KEY to use Kling AI Avatar v2 Pro (model kling_avatar_v2_pro).\n"
        "Local: clone https://github.com/OpenTalker/SadTalker and set SADTALKER_PATH "
        "(PyTorch + GPU required)."
    )

    agent_skills = ["ffmpeg"]
    fallback = "lip_sync"

    capabilities = [
        "photo_to_video",
        "face_animation",
        "audio_driven_animation",
    ]

    input_schema = {
        "type": "object",
        "required": ["image_path", "audio_path"],
        "properties": {
            "image_path": {
                "type": "string",
                "description": "Path to source face photo",
            },
            "audio_path": {
                "type": "string",
                "description": "Path to driving audio file",
            },
            "output_path": {
                "type": "string",
                "description": "Output video path (default: {stem}_talking.mp4)",
            },
            "model": {
                "type": "string",
                "enum": ["sadtalker", "musetalk", "kling_avatar_v2_pro", "sync_3_image"],
                "default": "sadtalker",
                "description": "Model to use for face animation (kling_avatar_v2_pro and sync_3_image are hosted on fal)",
            },
            "prompt": {
                "type": "string",
                "description": "Hosted models: optional motion/performance direction",
            },
            "duration_seconds": {
                "type": "number",
                "description": "Audio length, used only for hosted cost estimation",
            },
            "queue_record_path": {
                "type": "string",
                "description": "Hosted models: file recording the queue job; an existing record blocks resubmission",
            },
            "expression_scale": {
                "type": "number",
                "default": 1.0,
                "description": "Expression intensity multiplier",
            },
            "still_mode": {
                "type": "boolean",
                "default": False,
                "description": "Only animate mouth, keep head still",
            },
            "preprocess": {
                "type": "string",
                "enum": ["crop", "resize", "full"],
                "default": "crop",
                "description": "Face preprocessing mode",
            },
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=2, ram_mb=4096, vram_mb=4096, disk_mb=2000
    )
    idempotency_key_fields = ["image_path", "audio_path", "model", "expression_scale", "still_mode"]
    side_effects = ["writes video file to output_path"]
    user_visible_verification = [
        "Watch generated video for lip-sync accuracy",
        "Check for face distortion or unnatural artifacts",
    ]

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> ToolStatus:
        """Available with hosted fal access or a local SadTalker install."""
        if get_fal_api_key():
            return ToolStatus.AVAILABLE

        # 1. SADTALKER_PATH env var pointing to cloned repo
        sadtalker_path = os.environ.get("SADTALKER_PATH", "")
        if sadtalker_path and Path(sadtalker_path).is_dir():
            return ToolStatus.AVAILABLE

        # 2. Installed as a Python package
        try:
            import sadtalker  # noqa: F401
            return ToolStatus.AVAILABLE
        except ImportError:
            pass

        return ToolStatus.UNAVAILABLE

    # ------------------------------------------------------------------
    # Cost & runtime estimates
    # ------------------------------------------------------------------

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        """Hosted models bill per output second; local models are free."""
        rate = FAL_AVATAR_USD_PER_SECOND.get(inputs.get("model", "sadtalker"), 0.0)
        return round(rate * float(inputs.get("duration_seconds", 0)), 2)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        # SadTalker typically takes 30-120s depending on audio length
        return 60.0

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        image_path = Path(inputs["image_path"])
        audio_path = Path(inputs["audio_path"])

        if not image_path.exists():
            return ToolResult(success=False, error=f"Image not found: {image_path}")
        if not audio_path.exists():
            return ToolResult(success=False, error=f"Audio not found: {audio_path}")

        model = inputs.get("model", "sadtalker")
        output_path = Path(
            inputs.get("output_path", str(image_path.with_stem(f"{image_path.stem}_talking").with_suffix(".mp4")))
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)

        start = time.time()

        try:
            if model in FAL_AVATAR_ENDPOINTS:
                request_info = run_fal_avatar(model, image_path, audio_path, output_path, inputs)
                result = ToolResult(
                    success=True,
                    data={"output": str(output_path), "backend": "fal", **request_info},
                    artifacts=[str(output_path)],
                    model=FAL_AVATAR_ENDPOINTS[model],
                )
            elif model == "sadtalker":
                result = self._run_sadtalker(inputs, image_path, audio_path, output_path)
            elif model == "musetalk":
                result = self._run_musetalk(inputs, image_path, audio_path, output_path)
            else:
                return ToolResult(
                    success=False,
                    error=f"Unknown model: {model}. Supported: sadtalker, musetalk, kling_avatar_v2_pro, sync_3_image",
                )
        except Exception as e:
            return ToolResult(success=False, error=f"Talking head generation failed: {e}")

        result.duration_seconds = round(time.time() - start, 2)
        return result

    def _run_sadtalker(
        self,
        inputs: dict[str, Any],
        image_path: Path,
        audio_path: Path,
        output_path: Path,
    ) -> ToolResult:
        """Run SadTalker inference via subprocess."""
        sadtalker_path = os.environ.get("SADTALKER_PATH", "")
        if not sadtalker_path or not Path(sadtalker_path).is_dir():
            return ToolResult(
                success=False,
                error="SADTALKER_PATH not set or directory does not exist.\n" + self.install_instructions,
            )

        sadtalker_dir = Path(sadtalker_path)
        result_dir = output_path.parent / "sadtalker_results"
        result_dir.mkdir(parents=True, exist_ok=True)

        expression_scale = inputs.get("expression_scale", 1.0)
        still_mode = inputs.get("still_mode", False)
        preprocess = inputs.get("preprocess", "crop")

        # Build SadTalker inference command
        cmd = [
            "python", str(sadtalker_dir / "inference.py"),
            "--driven_audio", str(audio_path),
            "--source_image", str(image_path),
            "--result_dir", str(result_dir),
            "--expression_scale", str(expression_scale),
            "--preprocess", preprocess,
        ]

        if still_mode:
            cmd.append("--still")

        self.run_command(cmd, cwd=sadtalker_dir, timeout=600)

        # Find the output video in result_dir (SadTalker names it automatically)
        generated = glob.glob(str(result_dir / "**" / "*.mp4"), recursive=True)
        if not generated:
            return ToolResult(
                success=False,
                error=f"No output video found in {result_dir}",
            )

        # Use the most recently created file
        generated.sort(key=os.path.getmtime, reverse=True)
        generated_path = Path(generated[0])

        # Move to the desired output path
        shutil.move(str(generated_path), str(output_path))

        return ToolResult(
            success=True,
            data={
                "model": "sadtalker",
                "image": str(image_path),
                "audio": str(audio_path),
                "output": str(output_path),
                "expression_scale": expression_scale,
                "still_mode": still_mode,
                "preprocess": preprocess,
                "format": "mp4",
            },
            artifacts=[str(output_path)],
            model="sadtalker",
        )

    def _run_musetalk(
        self,
        inputs: dict[str, Any],
        image_path: Path,
        audio_path: Path,
        output_path: Path,
    ) -> ToolResult:
        """MuseTalk support — placeholder for future implementation."""
        return ToolResult(
            success=False,
            error=(
                "MuseTalk support is not yet implemented. "
                "Use model='sadtalker' instead."
            ),
        )

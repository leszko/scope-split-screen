"""Pipeline that combines two video input frames into a split-screen output."""

import logging

import torch
import torch.nn.functional as F

from scope.core.pipelines.interface import Pipeline, Requirements

from .schema import SplitScreenConfig

logger = logging.getLogger(__name__)


class SplitScreenPipeline(Pipeline):
    """Produces a split-screen output from two video streams.

    Takes one frame from the "video" stream (top half) and one from the
    "video2" stream (bottom half). If only one stream is provided, the
    other half is filled with black.
    """

    def __init__(self, **kwargs):
        pass

    @classmethod
    def get_config_class(cls) -> type[SplitScreenConfig]:
        return SplitScreenConfig

    def prepare(self, **kwargs) -> Requirements:
        """Declare we need one frame from the primary video stream per call."""
        return Requirements(input_size=1)

    def __call__(self, **kwargs) -> dict:
        """Combine one frame from each stream vertically (video=top, video2=bottom).

        Args:
            **kwargs: Pipeline parameters.
                ``video``: list of tensors (1, H, W, C) in [0, 255] uint8 — top half.
                ``video2``: optional list of tensors (1, H, W, C) in [0, 255] uint8 — bottom half.
                ``output_height``, ``output_width``: combined output size.

        Returns:
            Dict with ``video`` key containing a single THWC tensor (1, H, W, 3) in [0, 1] range.
        """
        output_height = kwargs.get("output_height", 512)
        output_width = kwargs.get("output_width", 512)
        half_h = output_height // 2
        bottom_h = output_height - half_h

        frames1 = kwargs.get("video", []) or []
        frames2 = kwargs.get("video2", []) or []

        logger.debug(
            "split_screen: video=%d frames, video2=%d frames",
            len(frames1),
            len(frames2),
        )
        if len(frames1) == 0 and len(frames2) > 0:
            logger.warning(
                "split_screen: 'video' input is empty (top will be black); "
                "check that the upstream pipeline (e.g. yolo_mask) is connected to the 'video' port."
            )

        frame_top = frames1[0] if len(frames1) > 0 else None
        frame_bottom = frames2[0] if len(frames2) > 0 else None

        # Pick device from first available frame, otherwise CPU
        device = torch.device("cpu")
        if frame_top is not None:
            device = frame_top.device
        elif frame_bottom is not None:
            device = frame_bottom.device

        if frame_top is not None:
            top = self._resize_and_crop(frame_top, half_h, output_width)
        else:
            top = torch.zeros(1, half_h, output_width, 3, device=device, dtype=torch.float32)

        if frame_bottom is not None:
            bottom = self._resize_and_crop(frame_bottom, bottom_h, output_width)
        else:
            bottom = torch.zeros(1, bottom_h, output_width, 3, device=device, dtype=torch.float32)

        # Ensure same device (e.g. if one was black and created on CPU)
        if top.device != bottom.device:
            bottom = bottom.to(top.device)
        combined = torch.cat([top, bottom], dim=1)  # (1, H, W, 3)

        return {"video": combined}

    @staticmethod
    def _resize_and_crop(
        frame: torch.Tensor, target_h: int, target_w: int
    ) -> torch.Tensor:
        """Resize a frame to cover the target area then center-crop.

        Args:
            frame: (1, H, W, C) tensor in [0, 255] uint8.
            target_h: Desired height.
            target_w: Desired width.

        Returns:
            (1, target_h, target_w, 3) tensor in [0, 1] float range.
        """
        # Convert to float [0, 1]
        img = frame.float() / 255.0

        # Rearrange to (1, C, H, W) for F.interpolate
        img = img.permute(0, 3, 1, 2)

        _, _, h, w = img.shape

        # Scale so the frame covers the target area (cover scaling)
        scale = max(target_h / h, target_w / w)
        new_h = int(h * scale)
        new_w = int(w * scale)

        img = F.interpolate(img, size=(new_h, new_w), mode="bilinear", align_corners=False)

        # Center crop to target size
        y_start = (new_h - target_h) // 2
        x_start = (new_w - target_w) // 2
        img = img[:, :, y_start : y_start + target_h, x_start : x_start + target_w]

        # Back to (1, H, W, C)
        return img.permute(0, 2, 3, 1)

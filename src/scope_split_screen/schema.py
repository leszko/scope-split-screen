"""Configuration schema for the split-screen pipeline."""

from typing import ClassVar

from pydantic import Field

from scope.core.pipelines.base_schema import (
    BasePipelineConfig,
    ModeDefaults,
    input_size_field,
    ui_field_config,
)


class SplitScreenConfig(BasePipelineConfig):
    """Configuration for the split-screen pipeline."""

    pipeline_id: ClassVar[str] = "split-screen"
    pipeline_name: ClassVar[str] = "Split Screen"
    pipeline_description: ClassVar[str] = (
        "Produces a split-screen output from two video inputs: one frame from "
        "'video' (top half) and one from 'video2' (bottom half). "
        "If only one stream is connected, the other half is black."
    )

    inputs: ClassVar[list[str]] = ["video", "video2"]
    outputs: ClassVar[list[str]] = ["video"]

    artifacts: ClassVar[list] = []
    supports_prompts: ClassVar[bool] = False
    modified: ClassVar[bool] = True
    modes: ClassVar[dict[str, ModeDefaults]] = {
        "video": ModeDefaults(default=True, input_size=1),
    }

    input_size: int | None = input_size_field(default=1)

    output_height: int = Field(
        default=512,
        ge=64,
        description="Height of the split-screen output frame in pixels.",
        json_schema_extra=ui_field_config(order=1, label="Output Height"),
    )

    output_width: int = Field(
        default=512,
        ge=64,
        description="Width of the split-screen output frame in pixels.",
        json_schema_extra=ui_field_config(order=2, label="Output Width"),
    )

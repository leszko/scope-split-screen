"""Configuration schema for the combine streams pipeline."""

from typing import ClassVar

from pydantic import Field

from scope.core.pipelines.base_schema import (
    BasePipelineConfig,
    ModeDefaults,
    input_size_field,
    ui_field_config,
)


class CombineStreamsConfig(BasePipelineConfig):
    """Configuration for the combine streams pipeline."""

    pipeline_id: ClassVar[str] = "combine_streams"
    pipeline_name: ClassVar[str] = "Combine Streams"
    pipeline_description: ClassVar[str] = (
        "Combines two video inputs into a single stream: one frame from "
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
        description="Height of the combined output frame in pixels.",
        json_schema_extra=ui_field_config(order=1, label="Output Height"),
    )

    output_width: int = Field(
        default=512,
        ge=64,
        description="Width of the combined output frame in pixels.",
        json_schema_extra=ui_field_config(order=2, label="Output Width"),
    )

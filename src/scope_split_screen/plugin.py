"""Plugin class for Daydream Scope integration."""

import logging

from scope.core.plugins import hookimpl

from .pipeline import SplitScreenPipeline

logger = logging.getLogger(__name__)


class SplitScreenPlugin:
    """Scope plugin that combines two video streams into a split-screen output."""

    @hookimpl
    def register_pipelines(self, register):
        """Register the split-screen pipeline."""
        register(SplitScreenPipeline)
        logger.info("Registered split-screen pipeline")

"""Plugin class for Daydream Scope integration."""

import logging

from scope.core.plugins import hookimpl

from .pipeline import CombineStreamsPipeline

logger = logging.getLogger(__name__)


class CombineStreamsPlugin:
    """Scope plugin that combines two video streams into one output."""

    @hookimpl
    def register_pipelines(self, register):
        """Register the combine streams pipeline."""
        register(CombineStreamsPipeline)
        logger.info("Registered combine streams pipeline")

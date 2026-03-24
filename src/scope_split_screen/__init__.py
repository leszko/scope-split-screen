"""Split-screen plugin for Daydream Scope — stacks two video streams vertically."""

from .plugin import SplitScreenPlugin

plugin = SplitScreenPlugin()

__all__ = ["plugin", "SplitScreenPlugin"]

"""Combine two video streams into one output plugin for Daydream Scope."""

from .plugin import CombineStreamsPlugin

plugin = CombineStreamsPlugin()

__all__ = ["plugin", "CombineStreamsPlugin"]

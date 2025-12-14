"""Dashboard module - backwards compatibility wrapper.

This module now imports from the modular UI package.
"""

from .ui.dashboard import WebAlertDashboard, main

__all__ = ["WebAlertDashboard", "main"]

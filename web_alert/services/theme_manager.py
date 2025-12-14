"""Theme management service."""

import logging

import customtkinter as ctk

logger = logging.getLogger(__name__)


class ThemeManager:
    """Manages application theme."""

    def __init__(self, config_manager):
        """Initialize the theme manager.

        Args:
            config_manager: ConfigManager instance
        """
        self.config_manager = config_manager
        self.menu_bar = None

    def load_theme(self):
        """Load and apply saved theme."""
        theme = self.config_manager.get("theme", "light")
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")
        logger.info(f"Loaded theme: {theme}")

    def change_theme(self, theme: str, menu_recreate_callback=None):
        """Change the application theme.

        Args:
            theme: Theme to apply ('light', 'dark', or 'system')
            menu_recreate_callback: Optional callback to recreate menu bar
        """
        try:
            # Set the theme
            ctk.set_appearance_mode(theme)

            # Save preference
            self.config_manager.set("theme", theme)

            # Recreate menu bar with new theme colors if callback provided
            if menu_recreate_callback:
                menu_recreate_callback()

            logger.info(f"Theme changed to: {theme}")
        except Exception as e:
            logger.error(f"Failed to change theme: {e}")
            raise

    def get_current_theme(self) -> str:
        """Get the current theme.

        Returns:
            Current theme name
        """
        return self.config_manager.get("theme", "dark")

    def get_menu_colors(self) -> dict:
        """Get menu colors based on current theme.

        Returns:
            Dictionary with menu color configuration
        """
        theme = self.get_current_theme()

        if theme == "light":
            return {
                "bg": "#FFFFFF",
                "fg": "#1F2937",
                "active_bg": "#F3F4F6",
                "active_fg": "#7C3AED",
            }
        else:  # dark or system (default to dark colors)
            return {
                "bg": "#1E293B",
                "fg": "#F1F5F9",
                "active_bg": "#334155",
                "active_fg": "#A78BFA",
            }

    def get_colors(self) -> dict:
        """Get application color palette.

        Returns:
            Dictionary with color definitions
        """
        return {
            "primary": "#7C3AED",  # Vibrant purple
            "success": "#10B981",  # Emerald green
            "danger": "#EF4444",  # Modern red
            "warning": "#F59E0B",  # Amber
            "info": "#3B82F6",  # Bright blue
            "secondary": "#8B5CF6",  # Violet
            "muted": "#64748B",  # Slate gray
            "accent": "#EC4899",  # Pink accent
            "card_bg": ("gray90", "#1E293B"),  # Light/Dark mode
            "hover_primary": "#6D28D9",
            "hover_success": "#059669",
            "hover_danger": "#DC2626",
            "hover_info": "#2563EB",
            "text_primary": ("gray10", "gray95"),
            "text_secondary": ("gray30", "gray60"),
            "border": ("gray70", "#334155"),
        }

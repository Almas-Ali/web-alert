"""Configuration manager for web alert settings using database backend."""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration using database backend."""

    DEFAULT_SETTINGS = {
        "theme": "dark",
        "auto_start": "false",
        "log_changes": "true",
    }

    def __init__(self, db=None):
        """
        Initialize configuration manager.

        Args:
            db: ConfigDatabase instance (will be injected to avoid circular imports)
        """
        self.db = db
        logger.info("ConfigManager initialized with database backend")

    def set_database(self, db):
        """
        Set the database instance.

        Args:
            db: ConfigDatabase instance
        """
        self.db = db

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        if not self.db:
            logger.warning("Database not initialized, returning default")
            return self.DEFAULT_SETTINGS.get(key, default)

        value = self.db.get_setting(key, self.DEFAULT_SETTINGS.get(key, default))

        # Convert string booleans to actual booleans
        if value in ("true", "True"):
            return True
        elif value in ("false", "False"):
            return False

        return value if value is not None else default

    def set(self, key: str, value: Any) -> bool:
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value

        Returns:
            True if successful
        """
        if not self.db:
            logger.error("Database not initialized")
            return False

        # Convert boolean to string for storage
        if isinstance(value, bool):
            value = "true" if value else "false"

        return self.db.set_setting(key, str(value))

    def get_all(self) -> dict:
        """
        Get all configuration values.

        Returns:
            Dictionary of all settings
        """
        if not self.db:
            logger.warning("Database not initialized, returning defaults")
            return self.DEFAULT_SETTINGS.copy()

        return self.db.get_all_settings()

    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        if not self.db:
            logger.error("Database not initialized")
            return

        for key, value in self.DEFAULT_SETTINGS.items():
            self.db.set_setting(key, value)

        logger.info("Configuration reset to defaults")

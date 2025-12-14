"""Migration 001: Add tts_message column to configurations and active_jobs tables.

Revision: 001
Created: 2025-12-15
"""

import logging

from sqlalchemy import text
from sqlalchemy.engine import Engine

from ..migration_manager import Migration

logger = logging.getLogger(__name__)


class AddTtsMessage(Migration):
    """Add tts_message column for text-to-speech functionality."""

    version = "001"
    description = "Add tts_message column to configurations and active_jobs tables"

    def up(self, engine: Engine) -> bool:
        """
        Apply migration: Add tts_message column.

        Args:
            engine: SQLAlchemy engine

        Returns:
            True if successful
        """
        try:
            with engine.connect() as conn:
                # Check and add tts_message column to configurations table
                result = conn.execute(text("PRAGMA table_info(configurations)"))
                columns = [row[1] for row in result]

                if "tts_message" not in columns:
                    logger.info("Adding tts_message column to configurations table")
                    conn.execute(
                        text("ALTER TABLE configurations ADD COLUMN tts_message VARCHAR")
                    )
                    conn.commit()
                else:
                    logger.info("tts_message column already exists in configurations")

                # Check and add tts_message column to active_jobs table
                result = conn.execute(text("PRAGMA table_info(active_jobs)"))
                columns = [row[1] for row in result]

                if "tts_message" not in columns:
                    logger.info("Adding tts_message column to active_jobs table")
                    conn.execute(
                        text("ALTER TABLE active_jobs ADD COLUMN tts_message VARCHAR")
                    )
                    conn.commit()
                else:
                    logger.info("tts_message column already exists in active_jobs")

            return True

        except Exception as e:
            logger.error(f"Error in migration 001: {e}")
            return False

    def down(self, engine: Engine) -> bool:
        """
        Revert migration: Remove tts_message column.

        Note: SQLite does not support DROP COLUMN directly.
        This would require recreating tables.

        Args:
            engine: SQLAlchemy engine

        Returns:
            True if successful
        """
        logger.warning(
            "Downgrade not implemented: SQLite does not support DROP COLUMN"
        )
        return False


# Export migration instance
migration = AddTtsMessage()

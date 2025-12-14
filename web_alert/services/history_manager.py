"""History management service."""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class HistoryManager:
    """Manages configuration history."""

    def __init__(self, db):
        """Initialize the history manager.

        Args:
            db: ConfigDatabase instance
        """
        self.db = db

    def get_recent_configs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent configurations.

        Args:
            limit: Maximum number of configurations to return

        Returns:
            List of configuration dictionaries
        """
        return self.db.get_recent_configs(limit)

    def cleanup_old_configs(self, keep_count: int = 20):
        """Clean up old configurations.

        Args:
            keep_count: Number of recent configurations to keep
        """
        self.db.cleanup_old_configs(keep_count)
        logger.info(f"Cleaned up history, keeping {keep_count} most recent")

    def clear_all_history(self) -> int:
        """Clear all configuration history.

        Returns:
            Number of configurations deleted
        """
        from ..models import Configuration

        session = self.db._get_session()
        try:
            deleted = session.query(Configuration).delete()
            session.commit()
            logger.info(f"Deleted {deleted} configuration(s) from history")
            return deleted
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to clear history: {e}")
            raise
        finally:
            session.close()

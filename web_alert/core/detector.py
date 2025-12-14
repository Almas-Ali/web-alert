"""Change detection module for monitoring web content changes."""

import hashlib
import logging
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ChangeDetector:
    """Detects changes in web content."""

    def __init__(self, comparison_mode: str = "text"):
        """
        Initialize the change detector.

        Args:
            comparison_mode: Mode of comparison ('text', 'html', 'hash')
        """
        self.comparison_mode = comparison_mode
        self.previous_content: Optional[str] = None
        self.previous_hash: Optional[str] = None
        self.last_check: Optional[datetime] = None
        self.change_count: int = 0

    def detect_change(self, current_content: Optional[str]) -> bool:
        """
        Detect if content has changed.

        Args:
            current_content: Current content to check

        Returns:
            True if change detected, False otherwise
        """
        if current_content is None:
            logger.warning("Cannot detect change: current content is None")
            return False

        # First run - store initial content
        if self.previous_content is None:
            logger.info("First run - storing initial content")
            self._store_content(current_content)
            return False

        # Detect change based on mode
        changed = False

        if self.comparison_mode == "hash":
            changed = self._compare_hash(current_content)
        elif self.comparison_mode == "text":
            changed = self._compare_text(current_content)
        else:  # html
            changed = self._compare_html(current_content)

        if changed:
            self.change_count += 1
            logger.info(f"Change detected! Total changes: {self.change_count}")
            self._store_content(current_content)

        self.last_check = datetime.now()
        return changed

    def _store_content(self, content: str):
        """Store content for future comparison."""
        self.previous_content = content
        self.previous_hash = self._calculate_hash(content)

    def _calculate_hash(self, content: str) -> str:
        """Calculate SHA256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _compare_hash(self, current_content: str) -> bool:
        """Compare using hash."""
        current_hash = self._calculate_hash(current_content)
        return current_hash != self.previous_hash

    def _compare_text(self, current_content: str) -> bool:
        """Compare text content (normalized)."""
        # Normalize whitespace
        current_normalized = " ".join(current_content.split())
        previous_normalized = " ".join(self.previous_content.split())
        return current_normalized != previous_normalized

    def _compare_html(self, current_content: str) -> bool:
        """Compare full HTML content."""
        return current_content != self.previous_content

    def get_diff_info(self) -> Dict:
        """
        Get information about the detected change.

        Returns:
            Dictionary with change information
        """
        return {
            "last_check": self.last_check,
            "change_count": self.change_count,
            "previous_length": len(self.previous_content)
            if self.previous_content
            else 0,
            "comparison_mode": self.comparison_mode,
        }

    def reset(self):
        """Reset the detector state."""
        self.previous_content = None
        self.previous_hash = None
        self.last_check = None
        self.change_count = 0
        logger.info("Detector state reset")

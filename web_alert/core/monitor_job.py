"""Monitor job model for tracking individual URL monitoring."""

import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .alerter import Alerter
from .detector import ChangeDetector
from .scraper import WebScraper


@dataclass
class MonitorJob:
    """Represents a single monitoring job."""

    id: str
    url: str
    selector: str = ""
    check_interval: int = 60
    comparison_mode: str = "text"
    alert_sound: str = ""
    tts_message: str = ""
    timeout: int = 10

    # Runtime state
    is_running: bool = False
    scraper: Optional[WebScraper] = None
    detector: Optional[ChangeDetector] = None
    alerter: Optional[Alerter] = None
    thread: Optional[threading.Thread] = None

    # Statistics
    created_at: datetime = field(default_factory=datetime.now)
    last_check: Optional[datetime] = None
    changes_detected: int = 0
    alerts_played: int = 0
    status: str = "Idle"
    status_color: str = "gray"

    # Logs
    logs: list = field(default_factory=list)
    notes: str = ""

    def start(self):
        """Initialize components for this job."""
        import logging
        logger = logging.getLogger(__name__)
        
        self.scraper = WebScraper(timeout=self.timeout)
        self.detector = ChangeDetector(comparison_mode=self.comparison_mode)
        
        # Debug logging for TTS - use empty string as fallback
        tts_msg = self.tts_message if self.tts_message else ""
        logger.info(f"Job {self.id} starting with TTS message: '{tts_msg}'")
        
        self.alerter = Alerter(
            self.alert_sound if self.alert_sound else None,
            tts_msg if tts_msg else None
        )
        self.is_running = True
        self.status = "Running"
        self.status_color = "#2ecc71"

    def stop(self):
        """Stop monitoring this job."""
        self.is_running = False
        if self.scraper:
            self.scraper.close()
        self.status = "Stopped"
        self.status_color = "#e74c3c"

    def update_stats(self, changed: bool, message: str = ""):
        """Update job statistics."""
        self.last_check = datetime.now()
        if changed:
            self.changes_detected += 1
            self.alerts_played += 1

        # Add to logs
        self.add_log(
            message if message else ("Change detected!" if changed else "No changes")
        )

    def add_log(self, message: str):
        """Add a log entry."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)

        # Keep only last 100 entries
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "id": self.id,
            "url": self.url,
            "selector": self.selector,
            "check_interval": self.check_interval,
            "comparison_mode": self.comparison_mode,
            "alert_sound": self.alert_sound,
            "tts_message": self.tts_message,
            "timeout": self.timeout,
            "notes": self.notes,
        }

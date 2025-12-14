"""Active job model for persisting monitoring jobs."""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Integer, String, Text

from .base import Base


class ActiveJob(Base):
    """Active monitoring job that persists between sessions."""

    __tablename__ = "active_jobs"

    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    selector = Column(String)
    check_interval = Column(Integer, nullable=False)
    comparison_mode = Column(String, nullable=False)
    alert_sound = Column(String)
    tts_message = Column(String)
    timeout = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
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

    def __repr__(self):
        return f"<ActiveJob(id='{self.id}', url='{self.url[:30]}...')>"

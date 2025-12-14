"""Configuration model for storing monitoring settings."""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Integer, String, Text

from .base import Base


class Configuration(Base):
    """Configuration model for storing monitoring settings."""

    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, index=True)
    selector = Column(String)
    check_interval = Column(Integer, nullable=False)
    comparison_mode = Column(String, nullable=False)
    alert_sound = Column(String)
    timeout = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    last_used = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, index=True
    )
    use_count = Column(Integer, default=1)
    notes = Column(Text)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "url": self.url,
            "selector": self.selector,
            "check_interval": self.check_interval,
            "comparison_mode": self.comparison_mode,
            "alert_sound": self.alert_sound,
            "timeout": self.timeout,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "use_count": self.use_count,
            "notes": self.notes,
        }

    def __repr__(self):
        return f"<Configuration(id={self.id}, url='{self.url[:30]}...', use_count={self.use_count})>"

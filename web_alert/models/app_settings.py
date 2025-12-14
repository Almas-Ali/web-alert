"""Application settings model."""

from datetime import datetime

from sqlalchemy import Column, DateTime, String

from .base import Base


class AppSettings(Base):
    """Application-level settings."""

    __tablename__ = "app_settings"

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<AppSettings(key='{self.key}', value='{self.value}')>"

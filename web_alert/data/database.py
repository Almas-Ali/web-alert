"""Database module for storing configuration history using SQLAlchemy ORM."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import create_engine, desc, func, or_
from sqlalchemy.orm import Session, sessionmaker

from ..migrations import MigrationManager
from ..models import ActiveJob, AppSettings, Base, Configuration

logger = logging.getLogger(__name__)


class ConfigDatabase:
    """Manages configuration history using SQLAlchemy ORM."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        if db_path:
            self.db_path = Path(db_path)
        else:
            base_dir = Path(__file__).parent.parent.parent
            self.db_path = base_dir / "web_alert_store.db"

        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create engine and session
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Create tables
        Base.metadata.create_all(self.engine)
        
        # Run migrations
        self._run_migrations()
        
        logger.info(f"Database initialized at {self.db_path}")
    
    def _run_migrations(self):
        """Run all database migrations automatically from versions directory."""
        try:
            migration_manager = MigrationManager(self.engine)
            
            # Auto-discover and run all migrations from versions directory
            migration_manager.run_migrations()
            
        except Exception as e:
            logger.error(f"Error running migrations: {e}")

    def _get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()

    def close(self):
        """Close database connections and dispose of the engine."""
        try:
            if hasattr(self, 'engine') and self.engine:
                self.engine.dispose()
                logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing database: {e}")

    def save_config(self, config: Dict[str, Any], notes: str = "") -> int:
        """
        Save a configuration to the database.

        Args:
            config: Configuration dictionary
            notes: Optional notes about this configuration

        Returns:
            Configuration ID
        """
        session = self._get_session()
        try:
            # Check if similar config exists
            existing = (
                session.query(Configuration)
                .filter(
                    Configuration.url == config.get("url", ""),
                    Configuration.selector == config.get("selector", ""),
                    Configuration.comparison_mode
                    == config.get("comparison_mode", "text"),
                )
                .first()
            )

            if existing:
                # Update existing configuration
                existing.check_interval = config.get("check_interval", 60)
                existing.alert_sound = config.get("alert_sound", "")
                existing.tts_message = config.get("tts_message", "")
                existing.timeout = config.get("timeout", 10)
                existing.last_used = datetime.now()
                existing.use_count += 1
                if notes:
                    existing.notes = notes

                session.commit()
                config_id = existing.id
                logger.info(f"Updated existing configuration #{config_id}")
            else:
                # Insert new configuration
                new_config = Configuration(
                    url=config.get("url", ""),
                    selector=config.get("selector", ""),
                    check_interval=config.get("check_interval", 60),
                    comparison_mode=config.get("comparison_mode", "text"),
                    alert_sound=config.get("alert_sound", ""),
                    tts_message=config.get("tts_message", ""),
                    timeout=config.get("timeout", 10),
                    notes=notes,
                )
                session.add(new_config)
                session.commit()
                config_id = new_config.id
                logger.info(f"Saved new configuration #{config_id}")

            return config_id

        except Exception as e:
            session.rollback()
            logger.error(f"Error saving configuration: {e}")
            return -1
        finally:
            session.close()

    def get_recent_configs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent configurations ordered by last used.

        Args:
            limit: Maximum number of configurations to return

        Returns:
            List of configuration dictionaries
        """
        session = self._get_session()
        try:
            configs = (
                session.query(Configuration)
                .order_by(desc(Configuration.last_used))
                .limit(limit)
                .all()
            )

            return [config.to_dict() for config in configs]

        except Exception as e:
            logger.error(f"Error getting recent configs: {e}")
            return []
        finally:
            session.close()

    def get_config_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get the most recent configuration for a specific URL.

        Args:
            url: The URL to search for

        Returns:
            Configuration dictionary or None
        """
        session = self._get_session()
        try:
            config = (
                session.query(Configuration)
                .filter(Configuration.url == url)
                .order_by(desc(Configuration.last_used))
                .first()
            )

            return config.to_dict() if config else None

        except Exception as e:
            logger.error(f"Error getting config by URL: {e}")
            return None
        finally:
            session.close()

    def get_config_by_id(self, config_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a configuration by its ID.

        Args:
            config_id: Configuration ID

        Returns:
            Configuration dictionary or None
        """
        session = self._get_session()
        try:
            config = (
                session.query(Configuration)
                .filter(Configuration.id == config_id)
                .first()
            )

            return config.to_dict() if config else None

        except Exception as e:
            logger.error(f"Error getting config by ID: {e}")
            return None
        finally:
            session.close()

    def search_configs(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search configurations by URL or notes.

        Args:
            search_term: Search term

        Returns:
            List of matching configurations
        """
        session = self._get_session()
        try:
            search_pattern = f"%{search_term}%"
            configs = (
                session.query(Configuration)
                .filter(
                    or_(
                        Configuration.url.like(search_pattern),
                        Configuration.notes.like(search_pattern),
                    )
                )
                .order_by(desc(Configuration.last_used))
                .all()
            )

            return [config.to_dict() for config in configs]

        except Exception as e:
            logger.error(f"Error searching configs: {e}")
            return []
        finally:
            session.close()

    def delete_config(self, config_id: int) -> bool:
        """
        Delete a configuration by ID.

        Args:
            config_id: Configuration ID to delete

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            config = (
                session.query(Configuration)
                .filter(Configuration.id == config_id)
                .first()
            )

            if config:
                session.delete(config)
                session.commit()
                logger.info(f"Deleted configuration #{config_id}")
                return True
            return False

        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting config: {e}")
            return False
        finally:
            session.close()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary with statistics
        """
        session = self._get_session()
        try:
            # Total configurations
            total = session.query(func.count(Configuration.id)).scalar()

            # Most used configuration
            most_used = (
                session.query(Configuration)
                .order_by(desc(Configuration.use_count))
                .first()
            )

            # Total usage count
            total_uses = session.query(func.sum(Configuration.use_count)).scalar() or 0

            return {
                "total_configs": total,
                "most_used_url": most_used.url if most_used else None,
                "most_used_count": most_used.use_count if most_used else 0,
                "total_uses": total_uses,
            }

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
        finally:
            session.close()

    def cleanup_old_configs(self, keep_count: int = 50):
        """
        Remove old configurations, keeping only the most recent ones.

        Args:
            keep_count: Number of configurations to keep
        """
        session = self._get_session()
        try:
            # Get IDs to keep
            ids_to_keep = (
                session.query(Configuration.id)
                .order_by(desc(Configuration.last_used))
                .limit(keep_count)
                .all()
            )

            keep_ids = [id_tuple[0] for id_tuple in ids_to_keep]

            # Delete all except those to keep
            if keep_ids:
                deleted = (
                    session.query(Configuration)
                    .filter(~Configuration.id.in_(keep_ids))
                    .delete(synchronize_session=False)
                )

                session.commit()

                if deleted > 0:
                    logger.info(f"Cleaned up {deleted} old configurations")

        except Exception as e:
            session.rollback()
            logger.error(f"Error cleaning up configs: {e}")
        finally:
            session.close()

    # Active Jobs Management

    def save_active_job(self, job_data: Dict[str, Any]) -> bool:
        """
        Save an active job to persist between sessions.

        Args:
            job_data: Job data dictionary

        Returns:
            True if successful
        """
        session = self._get_session()
        try:
            # Check if job already exists
            existing = (
                session.query(ActiveJob).filter(ActiveJob.id == job_data["id"]).first()
            )

            if existing:
                # Update existing job
                existing.url = job_data["url"]
                existing.selector = job_data.get("selector", "")
                existing.check_interval = job_data["check_interval"]
                existing.comparison_mode = job_data["comparison_mode"]
                existing.alert_sound = job_data.get("alert_sound", "")
                existing.tts_message = job_data.get("tts_message", "")
                existing.timeout = job_data.get("timeout", 10)
                existing.notes = job_data.get("notes", "")
            else:
                # Create new job
                new_job = ActiveJob(
                    id=job_data["id"],
                    url=job_data["url"],
                    selector=job_data.get("selector", ""),
                    check_interval=job_data["check_interval"],
                    comparison_mode=job_data["comparison_mode"],
                    alert_sound=job_data.get("alert_sound", ""),
                    tts_message=job_data.get("tts_message", ""),
                    timeout=job_data.get("timeout", 10),
                    notes=job_data.get("notes", ""),
                )
                session.add(new_job)

            session.commit()
            logger.info(f"Saved active job {job_data['id']}")
            return True

        except Exception as e:
            session.rollback()
            logger.error(f"Error saving active job: {e}")
            return False
        finally:
            session.close()

    def get_active_jobs(self) -> List[Dict[str, Any]]:
        """
        Get all active jobs.

        Returns:
            List of active job dictionaries
        """
        session = self._get_session()
        try:
            jobs = session.query(ActiveJob).all()
            return [job.to_dict() for job in jobs]

        except Exception as e:
            logger.error(f"Error getting active jobs: {e}")
            return []
        finally:
            session.close()

    def delete_active_job(self, job_id: str) -> bool:
        """
        Delete an active job.

        Args:
            job_id: Job ID to delete

        Returns:
            True if successful
        """
        session = self._get_session()
        try:
            job = session.query(ActiveJob).filter(ActiveJob.id == job_id).first()

            if job:
                session.delete(job)
                session.commit()
                logger.info(f"Deleted active job {job_id}")
                return True
            return False

        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting active job: {e}")
            return False
        finally:
            session.close()

    def clear_all_active_jobs(self) -> bool:
        """
        Clear all active jobs.

        Returns:
            True if successful
        """
        session = self._get_session()
        try:
            deleted = session.query(ActiveJob).delete()
            session.commit()
            logger.info(f"Cleared {deleted} active jobs")
            return True

        except Exception as e:
            session.rollback()
            logger.error(f"Error clearing active jobs: {e}")
            return False
        finally:
            session.close()

    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an application setting.

        Args:
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value or default
        """
        session = self._get_session()
        try:
            setting = session.query(AppSettings).filter(AppSettings.key == key).first()

            return setting.value if setting else default

        except Exception as e:
            logger.error(f"Error getting setting {key}: {e}")
            return default
        finally:
            session.close()

    def set_setting(self, key: str, value: str) -> bool:
        """
        Set an application setting.

        Args:
            key: Setting key
            value: Setting value

        Returns:
            True if successful
        """
        session = self._get_session()
        try:
            setting = session.query(AppSettings).filter(AppSettings.key == key).first()

            if setting:
                setting.value = value
                setting.updated_at = datetime.now()
            else:
                setting = AppSettings(key=key, value=value)
                session.add(setting)

            session.commit()
            logger.info(f"Set setting {key} = {value}")
            return True

        except Exception as e:
            session.rollback()
            logger.error(f"Error setting {key}: {e}")
            return False
        finally:
            session.close()

    def get_all_settings(self) -> Dict[str, str]:
        """
        Get all application settings.

        Returns:
            Dictionary of settings
        """
        session = self._get_session()
        try:
            settings = session.query(AppSettings).all()
            return {s.key: s.value for s in settings}

        except Exception as e:
            logger.error(f"Error getting all settings: {e}")
            return {}
        finally:
            session.close()

    def delete_setting(self, key: str) -> bool:
        """
        Delete an application setting.

        Args:
            key: Setting key

        Returns:
            True if successful
        """
        session = self._get_session()
        try:
            setting = session.query(AppSettings).filter(AppSettings.key == key).first()

            if setting:
                session.delete(setting)
                session.commit()
                logger.info(f"Deleted setting {key}")
                return True
            return False

        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting setting {key}: {e}")
            return False
        finally:
            session.close()

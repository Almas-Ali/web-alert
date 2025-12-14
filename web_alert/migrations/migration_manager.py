"""Migration manager for running database migrations."""

import importlib
import logging
from pathlib import Path
from typing import Any, Dict, List

from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class Migration:
    """Base class for database migrations."""

    version: str = "000"
    description: str = ""

    def up(self, engine: Engine) -> bool:
        """
        Apply the migration.

        Args:
            engine: SQLAlchemy engine

        Returns:
            True if successful
        """
        raise NotImplementedError

    def down(self, engine: Engine) -> bool:
        """
        Revert the migration (optional).

        Args:
            engine: SQLAlchemy engine

        Returns:
            True if successful
        """
        raise NotImplementedError


class MigrationManager:
    """Manages database migrations."""

    def __init__(self, engine: Engine):
        """
        Initialize migration manager.

        Args:
            engine: SQLAlchemy engine
        """
        self.engine = engine
        self._ensure_migration_table()

    def _ensure_migration_table(self):
        """Create migrations tracking table if it doesn't exist."""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text(
                        """
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        version VARCHAR(50) PRIMARY KEY,
                        description TEXT,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                    )
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Error creating migrations table: {e}")

    def _get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version FROM schema_migrations"))
                return [row[0] for row in result]
        except Exception as e:
            logger.error(f"Error getting applied migrations: {e}")
            return []

    def _mark_migration_applied(self, version: str, description: str):
        """Mark a migration as applied."""
        try:
            with self.engine.connect() as conn:
                conn.execute(
                    text(
                        "INSERT INTO schema_migrations (version, description) VALUES (:version, :description)"
                    ),
                    {"version": version, "description": description},
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Error marking migration {version} as applied: {e}")

    def _discover_migrations(self) -> List[Migration]:
        """
        Automatically discover and load migration files from versions directory.
        
        Returns:
            List of migration instances
        """
        migrations = []
        migrations_dir = Path(__file__).parent / "versions"
        
        if not migrations_dir.exists():
            logger.warning(f"Migrations directory not found: {migrations_dir}")
            return migrations
        
        # Find all Python files in versions directory (except __init__.py)
        migration_files = sorted([
            f for f in migrations_dir.glob("*.py")
            if f.name != "__init__.py" and not f.name.startswith("_")
        ])
        
        for migration_file in migration_files:
            try:
                # Import the migration module dynamically
                module_name = f"web_alert.migrations.versions.{migration_file.stem}"
                module = importlib.import_module(module_name)
                
                # Get the migration instance
                if hasattr(module, "migration"):
                    migration = module.migration
                    migrations.append(migration)
                    logger.debug(f"Loaded migration: {migration.version} - {migration.description}")
                else:
                    logger.warning(f"Migration file {migration_file.name} has no 'migration' attribute")
                    
            except Exception as e:
                logger.error(f"Error loading migration {migration_file.name}: {e}")
        
        return migrations
    
    def run_migrations(self, migrations: List[Migration] = None):
        """
        Run all pending migrations.

        Args:
            migrations: Optional list of migration instances. If None, auto-discovers migrations.
        """
        # Auto-discover migrations if not provided
        if migrations is None:
            migrations = self._discover_migrations()
        
        if not migrations:
            logger.info("No migrations found")
            return
        
        applied = self._get_applied_migrations()
        pending = [m for m in migrations if m.version not in applied]

        if not pending:
            logger.info("No pending migrations")
            return

        logger.info(f"Found {len(pending)} pending migration(s)")

        for migration in sorted(pending, key=lambda m: m.version):
            try:
                logger.info(
                    f"Applying migration {migration.version}: {migration.description}"
                )
                success = migration.up(self.engine)

                if success:
                    self._mark_migration_applied(
                        migration.version, migration.description
                    )
                    logger.info(f"Successfully applied migration {migration.version}")
                else:
                    logger.error(f"Failed to apply migration {migration.version}")

            except Exception as e:
                logger.error(f"Error applying migration {migration.version}: {e}")

    def get_migration_status(self) -> Dict[str, Any]:
        """
        Get current migration status.

        Returns:
            Dictionary with migration status information
        """
        applied = self._get_applied_migrations()
        return {
            "applied_count": len(applied),
            "applied_versions": applied,
        }

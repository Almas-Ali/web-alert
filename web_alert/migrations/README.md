# Database Migrations

This folder contains database migrations for Web Alert.

## Structure

```
migrations/
├── __init__.py                    # Package initialization
├── migration_manager.py           # Migration runner and manager
├── versions/                      # Migration versions
│   ├── __init__.py
│   └── 001_add_tts_message.py    # First migration
└── README.md                      # This file
```

## How Migrations Work

1. **Automatic Execution**: Migrations run automatically when the database is initialized
2. **Tracking**: Applied migrations are tracked in the `schema_migrations` table
3. **Idempotent**: Migrations check if changes are already applied before running
4. **Sequential**: Migrations are executed in version order (001, 002, 003, etc.)

## Creating a New Migration

### 1. Create a new migration file

Create a new file in `versions/` with the naming pattern:
```
{version}_{description}.py
```

Example: `002_add_notification_settings.py`

### 2. Use the migration template

```python
"""Migration {version}: Description of what this migration does.

Revision: {version}
Created: {date}
"""

import logging
from sqlalchemy import text
from sqlalchemy.engine import Engine
from ..migration_manager import Migration

logger = logging.getLogger(__name__)


class YourMigrationName(Migration):
    """Brief description of the migration."""
    
    version = "{version}"
    description = "Description for tracking"
    
    def up(self, engine: Engine) -> bool:
        """
        Apply the migration.
        
        Args:
            engine: SQLAlchemy engine
            
        Returns:
            True if successful
        """
        try:
            with engine.connect() as conn:
                # Your migration code here
                conn.execute(text("ALTER TABLE ..."))
                conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error in migration {self.version}: {e}")
            return False
    
    def down(self, engine: Engine) -> bool:
        """
        Revert the migration (optional).
        
        Note: SQLite has limited ALTER TABLE support.
        
        Args:
            engine: SQLAlchemy engine
            
        Returns:
            True if successful
        """
        # Implement rollback if possible
        return False


# Export migration instance
migration = YourMigrationName()
```

### 3. Register the migration

Add your migration to the list in `database.py`:

```python
from ..migrations.versions.002_your_migration import migration as migration_002

# In _run_migrations method:
migrations = [
    migration_001,
    migration_002,  # Add your migration here
]
```

## Migration Best Practices

### ✅ Do:
- **Test thoroughly** before committing
- **Keep migrations small** and focused on one change
- **Document clearly** what the migration does
- **Check for existing columns** before adding them
- **Use transactions** when possible
- **Log all actions** for debugging

### ❌ Don't:
- **Don't modify existing migrations** once they're committed
- **Don't delete old migrations** - they're part of the history
- **Don't rely on model classes** - migrations should be independent
- **Don't forget to commit** database transactions

## SQLite Limitations

SQLite has limited ALTER TABLE support:
- ✅ ADD COLUMN (supported)
- ❌ DROP COLUMN (not supported)
- ❌ ALTER COLUMN (not supported)
- ❌ RENAME COLUMN (only in SQLite 3.25+)

For unsupported operations, you need to:
1. Create a new table with the desired schema
2. Copy data from the old table
3. Drop the old table
4. Rename the new table

## Checking Migration Status

The `schema_migrations` table tracks applied migrations:

```sql
SELECT * FROM schema_migrations ORDER BY applied_at;
```

Columns:
- `version`: Migration version number
- `description`: Migration description
- `applied_at`: Timestamp when migration was applied

## Example Migrations

### Adding a Column
```python
conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR"))
```

### Creating a Table
```python
conn.execute(text('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
'''))
```

### Adding an Index
```python
conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"))
```

## Troubleshooting

### Migration fails to apply
1. Check the logs for error messages
2. Verify the SQL syntax is correct for SQLite
3. Check if the table/column already exists
4. Ensure database has write permissions

### Migration applied but not working
1. Verify the migration logic is correct
2. Check if the migration entry is in `schema_migrations`
3. Restart the application to reload schema

### Need to rollback a migration
1. Implement the `down()` method
2. Manually execute the rollback SQL
3. Remove the entry from `schema_migrations`

## Version History

- **001**: Add tts_message column for text-to-speech functionality

---

For more information about SQLAlchemy migrations, see:
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html)

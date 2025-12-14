# Developer Quick Reference

## Project Structure Quick Guide

```
web_alert/
├── models/          # Database models (ORM)
├── services/        # Business logic
├── ui/              # User interface
├── utils/           # Utilities
└── [core modules]   # Core functionality
```

## Common Development Tasks

### Adding a New Model

1. Create new file in `models/`
2. Import Base from `models.base`
3. Define model class
4. Add to `models/__init__.py`
5. Update database.py if needed

Example:
```python
from sqlalchemy import Column, String
from .base import Base

class NewModel(Base):
    __tablename__ = "new_table"
    id = Column(String, primary_key=True)
```

### Adding a New Service

1. Create file in `services/`
2. Create service class with `__init__()`
3. Inject dependencies
4. Add to `services/__init__.py`
5. Initialize in dashboard

Example:
```python
class NewService:
    def __init__(self, db):
        self.db = db
    
    def do_something(self):
        # Implementation
```

### Adding a New UI Component

1. Create file in `ui/`
2. Extend ctk.CTkToplevel or CTkFrame
3. Implement `__init__()` and `_create_widgets()`
4. Add to `ui/__init__.py`
5. Use in dashboard

Example:
```python
import customtkinter as ctk

class NewDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        # UI code
```

### Adding a Utility Function

1. Create or update file in `utils/`
2. Add function
3. Export in `utils/__init__.py`
4. Import where needed

## Import Patterns

### From UI to Services
```python
from ..services import JobManager, ThemeManager
```

### From Services to Models
```python
from ..models import Configuration, ActiveJob
```

### From Anywhere to Utils
```python
from ..utils import setup_logging, center_window
```

## Common Patterns

### Service Initialization
```python
# In __init__
self.db = ConfigDatabase()
self.service = ServiceClass(self.db)
```

### Dialog Creation
```python
def _show_dialog(self):
    dialog = MyDialog(self.root, self.db, callback=self._on_dialog_result)
```

### Thread-safe UI Updates
```python
self.root.after(0, lambda: self._update_ui())
```

### Database Operations
```python
session = self.db._get_session()
try:
    # Operations
    session.commit()
except Exception as e:
    session.rollback()
    raise
finally:
    session.close()
```

## Testing Patterns

### Service Testing
```python
def test_service():
    mock_db = Mock()
    service = MyService(mock_db)
    result = service.do_something()
    assert result == expected
```

### UI Testing (Future)
```python
def test_dialog():
    root = ctk.CTk()
    dialog = MyDialog(root, mock_db)
    # Test interactions
    root.destroy()
```

## Debugging

### Enable SQL Logging
```python
# In database.py
self.engine = create_engine(..., echo=True)
```

### Add Debug Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Check Job Status
```python
job = self.job_manager.get_job(job_id)
print(f"Status: {job.status}")
print(f"Running: {job.is_running}")
print(f"Logs: {job.logs}")
```

## Code Style

### Naming Conventions
- Classes: `PascalCase`
- Functions/Methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Docstrings
```python
def function_name(arg1: str, arg2: int) -> bool:
    """Short description.
    
    Args:
        arg1: Description
        arg2: Description
        
    Returns:
        Description
    """
```

### Type Hints
```python
from typing import Dict, List, Optional

def process(data: List[str]) -> Optional[Dict[str, int]]:
    ...
```

## Common Issues

### Import Errors
- Check relative imports (`..` for parent package)
- Ensure `__init__.py` exists
- Verify module is exported in `__init__.py`

### Database Errors
- Check if database is initialized
- Verify session management
- Look for commit/rollback issues

### UI Not Updating
- Use `root.after(0, callback)` for thread-safe updates
- Check if widget references are stored correctly
- Verify pack/grid is called

### Theme Not Applying
- Ensure theme is loaded before UI creation
- Check menu recreation after theme change
- Verify color keys exist in theme manager

## Performance Tips

### Database
- Use indexed columns for frequent queries
- Clean up old data regularly
- Batch operations when possible

### Threading
- Keep threads daemon for auto-cleanup
- Use events/flags for clean shutdown
- Avoid blocking UI thread

### Memory
- Limit log entry count
- Clean up widget references
- Use weak references for large collections

## Git Workflow

### Branch Naming
- feature/feature-name
- bugfix/bug-description
- refactor/what-was-refactored

### Commit Messages
```
type(scope): Short description

Longer description if needed

- Bullet point 1
- Bullet point 2
```

Types: feat, fix, refactor, docs, test, style

## Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in pyproject.toml
- [ ] No debug code left
- [ ] Logging levels appropriate
- [ ] Error handling complete
- [ ] UI tested on both themes

## Resources

- [CustomTkinter Docs](https://customtkinter.tomschimansky.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Python Threading](https://docs.python.org/3/library/threading.html)

## Getting Help

1. Check this guide
2. Review ARCHITECTURE.md
3. Look at existing similar code
4. Check logs for error details
5. Search issues on GitHub
6. Ask team member

## Quick Commands

```bash
# Run app
uv run main.py

# Install dependencies
uv sync

# Format code
uv run black .

# Lint
uv run ruff check .

# Run tests
uv run pytest

# Check dependencies
uv pip list
```

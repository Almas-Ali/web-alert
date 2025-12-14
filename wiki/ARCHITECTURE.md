# Web Alert - Architecture Documentation

## Overview
Web Alert is a modular web monitoring application built with Python and CustomTkinter, featuring a clean architecture with separated concerns.

## Project Structure

```
web_alert/
├── __init__.py
├── main.py                 # Application entry point
│
├── core/                   # Core business logic
│   ├── __init__.py
│   ├── alerter.py         # Alert system and sound notifications
│   ├── detector.py        # Change detection logic
│   ├── monitor_job.py     # MonitorJob dataclass
│   └── scraper.py         # Web scraping functionality
│
├── data/                   # Data access layer
│   ├── __init__.py
│   └── database.py        # Database operations and queries
│
├── models/                 # Database models (SQLAlchemy ORM)
│   ├── __init__.py
│   ├── base.py            # Base declarative class
│   ├── configuration.py   # Configuration history model
│   ├── active_job.py      # Active job persistence model
│   └── app_settings.py    # Application settings model
│
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── job_manager.py     # Job lifecycle management
│   ├── theme_manager.py   # Theme and appearance management
│   └── history_manager.py # Configuration history management
│
├── ui/                     # User interface components
│   ├── __init__.py
│   ├── dashboard.py       # Main dashboard window
│   ├── job_log_viewer.py  # Job log viewer dialog
│   └── add_job_dialog.py  # Add job dialog
│
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── logging_config.py  # Logging configuration
│   ├── window_utils.py    # Window utility functions
│   └── generate_sound.py  # Sound generation utility
│
├── config.py               # Configuration manager
└── dashboard.py            # Backwards compatibility wrapper

```

## Architecture Layers

### 1. Core Layer (core/)
- **Purpose**: Core business logic and domain models
- **Components**:
  - `Alerter`: Handles sound alerts and notifications
  - `ChangeDetector`: Detects changes in web content
  - `MonitorJob`: Job data model with monitoring logic
  - `WebScraper`: Fetches and parses web content
- **Benefits**: 
  - Encapsulates domain logic
  - Independent of UI and database
  - Highly testable

### 2. Data Layer (data/ + models/)
- **Purpose**: Database access and ORM models
- **Components**:
  - **data/database.py**: Database operations and queries
  - **models/**: SQLAlchemy ORM models
    - `Configuration`: Stores monitoring configuration history
    - `ActiveJob`: Persists active monitoring jobs between sessions
    - `AppSettings`: Application-level settings (theme, preferences)
    - `Base`: Shared declarative base
- **Technology**: SQLAlchemy ORM with SQLite backend
- **Features**:
  - Configuration CRUD operations
  - Active job persistence
  - Settings management
  - Automatic cleanup of old configurations

### 3. Service Layer (services/)
- **Purpose**: Business logic orchestration and state management
- **Components**:
  - `JobManager`: Manages job lifecycle (create, start, stop, remove)
  - `ThemeManager`: Handles theme switching and color schemes
  - `HistoryManager`: Manages configuration history
- **Benefits**: 
  - Separates business logic from UI
  - Coordinates between core and data layers
  - Reusable across different interfaces
  - Easier to test and maintain

### 4. UI Layer (ui/)
- **Purpose**: User interface components
- **Components**:
  - `WebAlertDashboard`: Main application window
  - `JobLogViewer`: Dialog for viewing job logs
  - `AddJobDialog`: Dialog for adding new jobs
- **Technology**: CustomTkinter for modern UI
- **Design**: Each dialog is self-contained and reusable

### 5. Utility Layer (utils/)
- **Purpose**: Common utility functions and helpers
- **Components**:
  - `logging_config`: Centralized logging setup
  - `window_utils`: Window positioning utilities
  - `generate_sound`: WAV sound file generation
- **Benefits**: DRY principle, code reusability

## Key Design Patterns

### 1. Separation of Concerns
- UI logic separated from business logic
- Database models separated from data access
- Services encapsulate specific functionality

### 2. Dependency Injection
- Services receive dependencies through constructors
- Makes testing easier and reduces coupling
- Example: `JobManager(db)`, `ThemeManager(config_manager)`

### 3. Factory Pattern
- `JobManager.create_job()` creates MonitorJob instances
- Centralizes job creation logic
- Handles both new and saved jobs

### 4. Observer Pattern
- Jobs notify UI of status changes
- Monitoring threads update job status
- UI reacts to job state changes

### 5. Facade Pattern
- `ConfigManager` provides simple interface to database settings
- `ThemeManager` abstracts theme switching complexity

## Data Flow

```
User Action (UI)
    ↓
Service Layer (Business Logic)
    ↓
Data Access Layer (Database Operations)
    ↓
Models (ORM)
    ↓
Database (SQLite)
```

## Module Responsibilities

### core/ (Business Logic)

#### core/alerter.py
- Play alert sounds (winsound on Windows)
- Manage alert sound files
- Track alert count
- Background thread support

#### core/detector.py
- Detect changes in web content
- Support multiple comparison modes (text, html, hash)
- Store previous content state
- Calculate content hashes

#### core/monitor_job.py
- MonitorJob dataclass
- Job state management (running, stopped)
- Integration with scraper, detector, alerter
- Log management
- Statistics tracking

#### core/scraper.py
- Fetch web content via HTTP
- Parse HTML with BeautifulSoup
- CSS selector support
- Timeout and error handling
- Session management

### data/ (Data Access)

#### data/database.py
- SQLAlchemy engine setup
- Session management
- CRUD operations for all models
- Configuration history queries
- Active job persistence
- Settings storage and retrieval
- Cleanup operations

### models/ (ORM Models)

#### models/base.py
- Shared SQLAlchemy declarative base
- Used by all model classes

#### models/configuration.py
- Configuration history table
- Tracks URL, selector, intervals
- Use count and last used tracking
- to_dict() serialization

#### models/active_job.py
- Active jobs table
- Persists jobs between sessions
- Job configuration storage

#### models/app_settings.py
- Application settings table
- Key-value storage
- Theme preferences, etc.

### services/ (Business Logic Layer)

#### services/job_manager.py
- Job creation and deletion
- Job lifecycle management (start/stop/remove)
- Thread management for monitoring
- Coordinates with database for persistence
- Bulk operations (start all, stop all)

#### services/theme_manager.py
- Theme loading and switching
- Color scheme management
- Menu color configuration
- Handles light/dark/system themes
- Color palette definitions

#### services/history_manager.py
- Retrieve recent configurations
- Clean up old configurations
- Clear all history
- Statistics and usage tracking

### ui/ (User Interface)

#### ui/dashboard.py (Main Application)
- Window initialization and layout
- Menu bar creation with themed colors
- Widget assembly
- Event handling
- Delegates business logic to services
- Job widget creation
- Status updates
- Window size: 600x700 pixels

#### ui/add_job_dialog.py
- Modal dialog for adding jobs
- Form validation
- History loading
- Sound file browsing
- Transient window positioning

#### ui/job_log_viewer.py
- Tabbed log viewer (Activity, Notes, Settings)
- Log export functionality
- Notes editing
- Auto-refresh capability
- Job statistics display

### utils/ (Utilities)

#### utils/logging_config.py
- Centralized logging setup
- File and console handlers
- Log directory creation

#### utils/window_utils.py
- Window centering utility
- Screen position calculation

#### utils/generate_sound.py
- WAV sound file generation
- Sine wave generation
- Envelope (fade in/out)
- Alert sound creation

### Root Level

#### dashboard.py (Backwards Compatibility)
- Imports from `ui.dashboard`
- Maintains existing import paths
- Exports `WebAlertDashboard` and `main`

#### config.py (Configuration Manager)
- Database-backed configuration
- Default settings management
- Get/set operations
- No JSON file dependency

## Configuration Management

### Storage
- All configuration stored in database (no JSON files)
- Settings table: key-value pairs
- Configuration table: monitoring config history
- Active jobs table: persisted jobs

### Theme System
- Supported: light, dark, system
- Stored in database
- Applied at startup
- Can be changed at runtime
- Updates menu colors automatically

## Job Lifecycle

1. **Creation**
   - User fills AddJobDialog
   - JobManager.create_job() called
   - Job saved to database
   - Widget created in UI

2. **Starting**
   - User clicks start button
   - JobManager.start_job() called
   - Thread spawned for monitoring
   - UI updated to show running state

3. **Monitoring**
   - Thread runs in background
   - Scrapes web content
   - Detects changes
   - Plays alerts
   - Updates job status
   - Logs activities

4. **Stopping**
   - User clicks stop button
   - JobManager.stop_job() sets flag
   - Thread exits gracefully
   - UI updated to show stopped state

5. **Removal**
   - User clicks remove button
   - Job stopped if running
   - Removed from database
   - Widget destroyed
   - JobManager cleanup

## Error Handling

### Logging
- Centralized in `utils/logging_config.py`
- File and console handlers
- INFO level for normal operation
- ERROR level for exceptions

### User Feedback
- Success messages for completed actions
- Error dialogs for failures
- Confirmation dialogs for destructive actions
- Status updates in job widgets

## Testing Considerations

### Testability Improvements
- Services can be tested independently
- Mock database for unit tests
- UI components isolated
- Clear interfaces between layers

### Test Strategy
- Unit tests for services
- Integration tests for database operations
- UI tests for critical workflows
- Mock external dependencies (web scraping)

## Migration Path

### Phase 1 (Completed) ✅
✅ Create modular structure with core/, data/, models/, services/, ui/, utils/
✅ Extract services (JobManager, ThemeManager, HistoryManager)
✅ Separate models into individual files
✅ Create utility functions
✅ Maintain backwards compatibility
✅ Move business logic to core/
✅ Centralize data access in data/
✅ Remove redundant gui.py
✅ Database-backed configuration (no JSON files)

### Phase 2 (Future)
- Add comprehensive unit tests
- Add integration tests
- Add API layer for remote control
- Plugin system for custom detectors
- Docker containerization
- CI/CD pipeline

## Performance Considerations

### Threading
- Each job runs in separate thread
- Daemon threads for auto-cleanup
- Thread-safe status updates
- GUI updates via root.after()

### Database
- SQLite for simplicity
- Indexed queries for performance
- Automatic cleanup of old data
- Connection pooling via SessionLocal

### Memory Management
- Jobs stored in dictionary
- Weak references considered for large deployments
- Logs limited by rotation

## Security Considerations

### Data Storage
- Local SQLite database
- No sensitive data encryption (future enhancement)
- File permissions handled by OS

### Web Scraping
- Timeout configuration
- Error handling for failed requests
- No automatic script execution

## Extension Points

### Adding New Features
1. **Custom Detectors**: Extend detector.py
2. **New Alert Types**: Extend alerter.py
3. **Additional UI**: Add to ui/ package
4. **New Services**: Add to services/ package

### Plugin Architecture (Future)
- Define plugin interfaces
- Load plugins dynamically
- Register with service layer
- Extend functionality without core changes

## Dependencies

### Core
- Python 3.13+
- SQLAlchemy >= 2.0.0
- customtkinter >= 5.2.0

### Monitoring
- requests
- beautifulsoup4
- lxml

### Optional
- pytest (testing)
- black (formatting)
- ruff (linting)

## Build and Deployment

### Development
```bash
uv sync
uv run main.py
```

### Testing
```bash
uv run pytest
```

### Packaging (Future)
```bash
uv build
```

## Conclusion

The modularized architecture provides:
- **Maintainability**: Clear separation of concerns
- **Testability**: Independent, testable components
- **Scalability**: Easy to add new features
- **Reusability**: Services can be used in different contexts
- **Clarity**: Each module has a single responsibility

This architecture follows SOLID principles and prepares the codebase for future enhancements while maintaining backwards compatibility.

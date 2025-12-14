# Changelog

All notable changes to Web Alert will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-15

### Added
- **Job Editing Functionality**: Edit existing job configurations without recreating them
  - New "✏️ Edit" button in job control panel
  - Edit dialog pre-fills all current job settings
  - Can modify URL, selector, interval, mode, sound, TTS message, and notes
  - Jobs must be stopped before editing
  - Changes are saved to database and UI updates automatically
- **Text-to-Speech Alerts (#2)**: Custom spoken messages when changes are detected
  - New "Text-to-Speech Message" field in Add/Edit Job dialogs
  - Messages spoken using system's text-to-speech engine (pyttsx3)
  - TTS and sound alerts are mutually exclusive (prevents audio overlap)
  - Messages saved and persisted with job configurations
  - Added `pyttsx3>=2.90` and `pywin32>=306` dependencies
- **Custom Application Icon**: Purple bell icon with red notification dot
  - Custom branding for window title bar and taskbar
  - Professional appearance with consistent design
  - Icon generation script included (`create_icon.py`)
  - Added `pillow>=10.0.0` dependency
- **Smart Sound File Browser**: Improved UX for selecting alert sounds
  - Opens in `web_alert/sounds` folder by default when field is empty
  - Opens in current file's directory when path exists
  - Provides better browsing experience
- **Interactive Tooltips**: Helpful hints on hover for icon buttons
  - Tooltip class for better user guidance
  - "View Logs", "Edit Job", "Remove Job" tooltips
- **Auto-Discovery Migration System**: Flexible database schema updates
  - Migrations auto-load from `migrations/versions/` folder
  - No hardcoded migration references needed
  - Migration 001: Added `tts_message` field to database

### Changed
- **TTS and Sound Alerts**: Now mutually exclusive to prevent audio overlap
  - If TTS message configured: Only TTS plays (no sound)
  - If no TTS message: Sound plays instead
- **Button Layout**: Reorganized job controls into compact 2-row layout
  - Start/Stop buttons (70px) in top row
  - Logs/Edit/Remove as icon buttons (45px) in bottom row
  - Remove button now red (#EF4444) for better visibility
- **Dialog Heights**: Increased Add/Edit Job dialog to 700px
- **Database Schema**: Added `tts_message` field to Configuration and ActiveJob models
- **Empty State Visibility**: Removed unreliable `winfo_viewable()` checks
- Updated database models to support TTS messages
- Enhanced Alerter class with TTS support and COM initialization for Windows
- Improved Add/Edit Job Dialog UI with TTS fields

### Fixed
- Fixed Tkinter error when job fields contain None values
- Fixed database session close error on application exit
- Fixed blank space in main monitoring area when jobs exist
- Fixed TTS threading issues with COM initialization and global lock

### Technical Details
- New file: `web_alert/ui/edit_job_dialog.py` - Full job editing dialog
- New file: `web_alert/migrations/migration_manager.py` - Auto-discovery system
- New file: `create_icon.py` - Icon generation script
- New files: `web_alert/icons/icon.png` and `icon.ico` - Application icons
- Modified: `web_alert/core/alerter.py` - TTS support with threading
- Modified: `web_alert/core/monitor_job.py` - Added `tts_message` field
- Modified: `web_alert/ui/dashboard.py` - Edit functionality, tooltips, button layout
- Modified: `web_alert/ui/add_job_dialog.py` - TTS field, smart file browser
- Modified: `web_alert/data/database.py` - Migration auto-discovery
- Modified database models: `Configuration` and `ActiveJob` with `tts_message`

## [1.0.2] - 2025-12-15

### Fixed
- Fixed blank space appearing in main monitoring area when jobs were active
- Changed empty state management to hide/show the entire container instead of just the label

## [1.0.1] - 2025-12-15

### Added
- Initial PyPI package configuration
- MIT License file
- Publishing guide (PUBLISHING.md)
- Updated pyproject.toml with complete metadata for PyPI

### Changed
- Reorganized project structure for PyPI distribution
- Updated README with PyPI installation instructions
- Added screenshot to README

## [1.0.0] - 2025-12-15

### Added
- Initial release of Web Alert
- Beautiful dashboard with modern GUI using CustomTkinter
- Multiple simultaneous website monitoring
- Three detection modes: Text, HTML, and Hash
- Custom alert sounds support
- Light, Dark, and System themes
- Configuration history for quick job reuse
- Individual job logs with export functionality
- Bulk operations (Start All, Stop All)
- Database-backed persistence using SQLAlchemy
- Modular architecture with clear separation of concerns
- Comprehensive documentation and developer guide

### Features
- Real-time status updates
- Adjustable check intervals
- CSS selector support for monitoring specific elements
- Activity tracking and statistics
- Notes support for each monitor
- Automatic saving and loading of jobs
- Window positioning utilities
- Sound generation utilities

---

## Legend

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

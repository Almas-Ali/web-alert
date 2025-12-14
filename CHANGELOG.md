# Changelog

All notable changes to Web Alert will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-15

### Added
- **Text-to-Speech Alerts (#2)**: Users can now add custom text messages that will be spoken when changes are detected
  - New "Text-to-Speech Message" field in Add Job dialog
  - Messages are spoken using the system's text-to-speech engine (pyttsx3)
  - Works alongside existing sound alerts
  - Messages are saved and persisted with job configurations
  - Added `pyttsx3>=2.90` dependency

### Changed
- Updated database schema to include `tts_message` field in Configuration and ActiveJob models
- Enhanced Alerter class to support both sound and TTS alerts
- Improved Add Job Dialog UI with new TTS message field and helpful info text
- Version bumped to 1.1.0

### Technical Details
- Added TTS functionality to `web_alert/core/alerter.py`
- Updated `web_alert/core/monitor_job.py` to include `tts_message` field
- Modified database models: `Configuration` and `ActiveJob`
- Updated `web_alert/ui/add_job_dialog.py` with TTS input field
- Enhanced dialog window height to 650px to accommodate new field

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

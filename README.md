# Web Alert 🔔

A modern dashboard application that monitors multiple websites simultaneously and alerts you with sound when changes are detected.

## Features

✨ **Dashboard Interface** - Manage multiple monitoring jobs from a single dashboard
🔄 **Parallel Monitoring** - Monitor multiple URLs simultaneously in separate threads
🔍 **Smart Change Detection** - Multiple comparison modes (text, HTML, hash)
🎯 **Flexible Monitoring** - Monitor entire pages or specific elements using CSS selectors
🔊 **Sound Alerts** - Customizable alert sounds with built-in default
⚙️ **Per-Job Configuration** - Each job has its own settings and intervals
📜 **Configuration History** - SQLAlchemy ORM database stores all configurations
📊 **Real-time Status** - Live status for each monitoring job
➕ **Easy Job Management** - Add, start, stop, and remove jobs on the fly
🕐 **Independent Intervals** - Each job runs on its own schedule
🔎 **History Integration** - Load previous configurations as new jobs

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

   Or install manually:
   ```bash
   pip install customtkinter requests beautifulsoup4 lxml
   ```

## Usage

### Running the Application

Simply run:
```bash
python main.py
```

Or use the installed command:
```bash
web-alert
```

### Quick Start Guide

1. **Launch the Dashboard**: Run the application to see the dashboard
2. **Add New Job**: Click "➕ Add New Job" button
3. **Configure Job Settings**:
   - Enter URL to monitor
   - (Optional) CSS Selector for specific elements
   - Set check interval in seconds
   - Choose comparison mode (text/HTML/hash)
   - (Optional) Select custom alert sound
4. **Start Monitoring**: Click "▶ Start" on the job
5. **Add More Jobs**: Repeat to monitor multiple URLs simultaneously
6. **Get Alerted**: Each job alerts independently when changes are detected

### Dashboard Features

**Job Management:**
- **Add New Job**: Create a new monitoring job with custom settings
- **Start/Stop Individual Jobs**: Control each job independently
- **Start/Stop All**: Batch control all jobs at once
- **Remove Jobs**: Delete jobs you no longer need
- **View Status**: See real-time status for each job

**Using History:**
- **Load from History**: When adding a job, click "📜 Load from History"
- **Add from History**: In History menu, add previous configs as new jobs
- **Auto-save**: All configurations are automatically saved to database

## Configuration Options

### Comparison Modes

- **Text Mode**: Compares normalized text content (ignores formatting)
- **HTML Mode**: Compares full HTML structure
- **Hash Mode**: Fast comparison using content hashing

### CSS Selectors

Use CSS selectors to monitor specific parts of a webpage:
- `#price` - Monitor element with ID "price"
- `.product-title` - Monitor elements with class "product-title"
- `div.content > p` - Monitor paragraphs inside div with class "content"
- Leave empty to monitor the entire page

## Project Structure

```
web-alert/
├── main.py                    # Entry point
├── web_alert/
│   ├── __init__.py
│   ├── dashboard.py           # Dashboard GUI application (NEW)
│   ├── gui.py                 # Legacy single-job GUI
│   ├── monitor_job.py         # Job model for tracking monitors (NEW)
│   ├── scraper.py             # Web scraping module
│   ├── detector.py            # Change detection logic
│   ├── alerter.py             # Sound alert system
│   ├── config.py              # Configuration management (database-backed)
│   ├── database.py            # SQLAlchemy ORM database (UPDATED)
│   └── generate_sound.py      # Sound generation utility
├── sounds/
│   └── alert.wav              # Default alert sound
├── logs/
│   └── web_alert.log          # Application logs
├── web_alert_store.db         # SQLite database (configurations + settings)
├── pyproject.toml
└── README.md
```

## Features in Detail

### Smart Change Detection

The system offers three comparison modes to suit different monitoring needs:

1. **Text Mode** (Default): Perfect for monitoring content changes while ignoring cosmetic updates
2. **HTML Mode**: Detects any structural changes in the page
3. **Hash Mode**: Ultra-fast comparison for detecting any changes

### Monitoring Options

- **Full Page Monitoring**: Leave CSS selector empty to monitor entire page
- **Element-Specific**: Use CSS selectors to focus on specific elements
- **Adjustable Intervals**: Set check frequency from 1 second to hours
- **Timeout Control**: Configure request timeout for slow-loading pages

### Alert System

- **Sound Alerts**: Plays sound when changes detected
- **Custom Sounds**: Use your own WAV files
- **Test Function**: Preview alert sound before monitoring
- **Visual Feedback**: Status updates and activity logs

### Status Tracking

- Current monitoring status
- Last check timestamp
- Next check countdown
- Total changes detected
- Total alerts played
- Active URL being monitored

## Use Cases

- **Price Monitoring**: Track price changes on e-commerce sites
- **News Updates**: Get alerted when news sites publish new articles
- **Product Availability**: Monitor "Out of Stock" to "In Stock" changes
- **Content Updates**: Track blog posts or website content changes
- **API Status Pages**: Monitor service status dashboards
- **Competition Tracking**: Watch competitor website updates

## Tips

1. **Start with longer intervals** (60+ seconds) to avoid overwhelming the target server
2. **Use CSS selectors** to monitor specific elements and reduce false positives
3. **Test your alert sound** before starting long monitoring sessions
4. **Save configurations** for frequently monitored sites
5. **Use text mode** to ignore dynamic ads and timestamps

## Requirements

- Python 3.8 or higher
- Windows (uses winsound for alerts)
- Internet connection

## Troubleshooting

**No sound playing?**
- Check that your sound entry is correct or leave empty for system default
- Test the alert sound using the "Test" button
- Ensure your system volume is not muted

**Changes not detected?**
- Try different comparison modes
- Check if the website loads correctly in your browser
- Verify the CSS selector matches existing elements
- Increase check interval if the site is slow to load

**High false positives?**
- Use CSS selectors to target specific content
- Switch to "text" mode to ignore formatting changes
- Increase the check interval

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Author

Created with ❤️ for web monitoring enthusiasts

---

**Note**: Please be respectful of website bandwidth and use reasonable check intervals. Excessive requests may be considered abuse.

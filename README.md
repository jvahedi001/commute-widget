# Commute Widget for macOS

A lightweight macOS menu bar widget that displays real-time commute times from your work location to home using Apple Maps data.

![Commute Widget Screenshot](screenshot.png)

## Features

- **Real-time Updates**: Automatically refreshes commute time every 5 minutes
- **Menu Bar Integration**: Displays commute time directly in your macOS menu bar with a car icon
- **Apple Maps Integration**: Uses native MapKit framework for accurate, live traffic data
- **Auto-start**: Runs automatically on login via LaunchAgent
- **Configurable**: Easy setup dialog to configure your home address
- **Manual Refresh**: Option to manually refresh commute time on demand

## Requirements

- macOS (Monterey or later recommended)
- Python 3.x
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jvahedi001/commute-widget.git
cd commute-widget
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Configure your home address:
   - On first run, a dialog will appear asking for your home address
   - The work address is currently hardcoded in `commute.py` (line 18)
   - You can change your home address later via the menu bar widget

4. Install as a LaunchAgent (auto-start on login):
```bash
./install.sh
```

The widget will now appear in your menu bar and start automatically on login.

## Configuration

### Customizing the Work Address

Edit `commute.py` and modify line 18:
```python
WORK_ADDRESS = "Your work address here"
```

### Changing Home Address

You can change your home address at any time by:
1. Clicking the widget in the menu bar
2. Selecting "Change Home Address"
3. Entering your new address

### Update Interval

To change how often the widget refreshes, edit line 20 in `commute.py`:
```python
UPDATE_INTERVAL = 300  # Time in seconds (default: 5 minutes)
```

## Usage

Once installed, the widget will:
- Display the current commute time in your menu bar (e.g., "🚗 33 min")
- Update automatically every 5 minutes
- Show "🚗 Loading..." while fetching new data

### Menu Options

Click the widget in the menu bar to access:
- **Refresh Now**: Manually update the commute time
- **Change Home Address**: Update your home address

## Uninstallation

To remove the widget:
```bash
./uninstall.sh
```

This will stop the widget and remove it from auto-starting on login.

## How It Works

The widget uses:
- **rumps**: Python library for creating macOS menu bar applications
- **MapKit**: Apple's native framework for directions and travel time calculations
- **CoreLocation**: For geocoding addresses to coordinates
- **LaunchAgent**: macOS service to run the widget automatically on login

The widget geocodes your home and work addresses, then uses MapKit to calculate driving time with current traffic conditions.

## Privacy

- All commute calculations are done locally using Apple's MapKit framework
- Your home and work addresses are stored only in `config.json` on your local machine
- No data is sent to external servers

## License

MIT License - feel free to modify and share!

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

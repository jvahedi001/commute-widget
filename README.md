# Commute Widget for macOS

A macOS menu bar widget that shows real-time commute times from work to home using Apple Maps.

## Motivation

This widget was created to solve a simple problem: knowing when to leave work to avoid heavy traffic. While macOS doesn't provide a built-in widget for monitoring commute times, and corporate device restrictions often prevent installing third-party applications, a lightweight Python script running in the menu bar provides an elegant solution that works within these constraints.

![Commute Widget Screenshot](screenshot.png)

## What It Does

Displays your current commute time in the menu bar with live traffic data. Updates automatically every minute and runs on startup.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jvahedi001/commute-widget.git
cd commute-widget
```

2. Install dependencies:
```bash
uv sync
```

3. Run the installer:
```bash
./install.sh
```

On first run, you'll be prompted to enter your home address.

## Configuration

**Important:** The work address is currently hardcoded to the VA office. You'll need to edit `commute.py` (line 18) to set your own work location:
```python
WORK_ADDRESS = "Your work address here"
```

You can change your home address anytime by clicking the widget and selecting "Change Home Address".

## Removal

```bash
./uninstall.sh
```

This stops the widget and removes it from startup.

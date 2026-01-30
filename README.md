# Commute Widget for macOS

A macOS menu bar widget that shows real-time commute times from work to home using Apple Maps.

![Commute Widget Screenshot](screenshot.png)

## What It Does

Displays your current commute time in the menu bar with live traffic data. Updates automatically every 5 minutes and runs on login.

## Installation

```bash
git clone https://github.com/jvahedi001/commute-widget.git
cd commute-widget
uv sync
./install.sh
```

On first run, you'll be prompted to enter your home address. The work address is hardcoded in `commute.py` line 18 - edit it to match your location.

## Removal

```bash
./uninstall.sh
```

# Commute Widget for macOS

A macOS menu bar widget that shows real-time commute times from work to home using Apple Maps.

## Why I Built This

For anyone else looking to see when to leave work to avoid traffic: there was no Apple background widget for this, and I couldn't install apps given the restrictions on my work machine. So I wrote a script that puts it in the menu bar and autostarts with login.

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

Edit your work address in `commute.py` (line 18):
```python
WORK_ADDRESS = "Your work address here"
```

You can change your home address anytime by clicking the widget and selecting "Change Home Address".

## Removal

```bash
./uninstall.sh
```

This stops the widget and removes it from startup.

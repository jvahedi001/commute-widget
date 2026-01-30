#!/bin/bash

echo "Installing Commute Widget..."

# Copy plist to LaunchAgents
cp com.commute-widget.plist ~/Library/LaunchAgents/

# Load the agent
launchctl load ~/Library/LaunchAgents/com.commute-widget.plist

# Start it
launchctl start com.commute-widget

echo "✓ Installed! Commute Widget will now start automatically on login."

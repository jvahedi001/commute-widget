#!/bin/bash

echo "Uninstalling Commute Widget..."

# Stop the agent
launchctl stop com.commute-widget

# Unload the agent
launchctl unload ~/Library/LaunchAgents/com.commute-widget.plist

# Remove the plist
rm ~/Library/LaunchAgents/com.commute-widget.plist

# Remove the config file
rm -f ~/Projects/commute-widget/config.json

echo "✓ Uninstalled! Commute Widget will no longer start automatically."

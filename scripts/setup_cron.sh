#!/bin/bash
# Setup auto-sync cron job

PROJECT=$1

if [ -z "$PROJECT" ]; then
    echo "Usage: setup_cron.sh <project-name>"
    exit 1
fi

# Add cron job for hourly sync
(crontab -l 2>/dev/null; echo "0 * * * * $HOME/.local/bin/ai-nexus sync $PROJECT >> $HOME/ai-nexus-sync.log 2>&1") | crontab -

echo "✅ Auto-sync enabled for $PROJECT"
echo "   Runs: Every hour"
echo "   Log: ~/ai-nexus-sync.log"
echo ""
echo "Check cron: crontab -l"
echo "View logs: tail -f ~/ai-nexus-sync.log"

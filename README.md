# ai-nexus - AI Dev Team Orchestration Platform

Multi-AI coordination platform for automated development workflows.

## Architecture
- Hub (Google Cloud): AI coordination & data sync
- Spoke (DO): Trading bot execution
- Auto-sync: Every hour via cron

## AI Agents
- Gemini: Data/pattern analysis (FREE)
- Grok: Social signals (ready to enable)
- Claude: Strategy design
- Claude Code: Implementation

## Quick Start
```bash
# Create project:
ai-nexus orchestrate new my-project --goal "Build X"

# Sync data:
ai-nexus sync my-project

# Assign AI tasks:
ai-nexus tasks assign my-project --auto

# Build consensus:
ai-nexus consensus my-project
```

## Status
- Infrastructure: Complete ✅
- Auto-sync: Running hourly ✅
- AI coordination: Working ✅
- First bot: In development (Claude Code)

## Cost
- Google Cloud: $0/month (free tier)
- Claude: $20/month
- Total: $20/month

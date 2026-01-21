# ai-nexus

Universal AI Collaboration Platform - Hub & Spoke Architecture

## Quick Start
```bash
# Install
pip install -e .

# Check version
ai-nexus --version

# Show status
ai-nexus status

# Initialize project
ai-nexus init solana-bot
```

## Architecture

- **Hub**: Google Cloud (ai-nexus coordination)
- **Spoke**: Digital Ocean (trading bot execution)
- **Connection**: SSH + data sync

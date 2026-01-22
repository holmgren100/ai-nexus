"""Project management and initialization"""
from pathlib import Path
import yaml
from datetime import datetime

class ProjectManager:
    """Manages AI-nexus projects"""
    
    def __init__(self):
        self.projects_dir = Path.home() / "ai-nexus" / "projects"
    
    def create_project(self, project_name, goal, agents, based_on=None):
        """Create new AI project with full structure"""
        
        project_dir = self.projects_dir / project_name
        
        # Create directory structure
        dirs = [
            project_dir / "shared-knowledge",
            project_dir / "data" / "raw" / "logs",
            project_dir / "data" / "raw" / "ml-data",
            project_dir / "data" / "analysis",
            project_dir / "code",
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create SYSTEM_STATE.md
        system_state = f"""# {project_name.upper()} - System State

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Status:** Initializing  
**Goal:** {goal}

---

## PROJECT OVERVIEW

**Objective:** {goal}
**AI Agents:** {', '.join(agents)}
**Based On:** {based_on or 'New project'}
**Created:** {datetime.now().strftime('%Y-%m-%d')}

---

## [ORCHESTRATOR] INITIALIZATION

Project structure created:
- Shared knowledge base (this file)
- Data directories (raw + analysis)
- Code repository link
- AI agent coordination

**Next Steps:**
1. Sync data from spoke servers
2. Assign analysis tasks to AI agents
3. Build consensus on strategy
4. Implement solution

---

## [GEMINI] DATA INSIGHTS

Status: Pending task assignment

---

## [GROK] SOCIAL ANALYSIS

Status: Pending task assignment

---

## [CLAUDE] STRATEGY DESIGN

Status: Pending task assignment

---

## [CONSENSUS] DECISIONS

No decisions yet - awaiting AI analysis

---

## CHANGELOG

- {datetime.now().strftime('%Y-%m-%d %H:%M')}: Project initialized by orchestrator
"""
        
        (project_dir / "shared-knowledge" / "SYSTEM_STATE.md").write_text(system_state)
        
        # Create AI_TASKS.md
        tasks = f"""# AI Tasks - {project_name}

## Active Tasks

None yet - run: ai-nexus tasks assign {project_name}

## Completed Tasks

None

## Task Queue

1. [GEMINI] Analyze historical trading data
2. [GROK] Analyze social patterns for successful tokens
3. [CLAUDE] Design strategy based on insights
4. [CLAUDE CODE] Implement strategy
"""
        
        (project_dir / "shared-knowledge" / "AI_TASKS.md").write_text(tasks)
        
        # Create config.yaml
        config = {
            'project': {
                'name': project_name,
                'goal': goal,
                'created': datetime.now().isoformat(),
                'based_on': based_on
            },
            'agents': {
                agent: {'enabled': True, 'status': 'pending'} 
                for agent in agents
            },
            'spoke_servers': {},
            'data_sources': []
        }
        
        if based_on:
            # Link to source project data
            config['spoke_servers']['trading'] = {
                'host': '209.38.229.243',
                'user': 'root',
                'ssh_key': '~/.ssh/id_ai_nexus',
                'paths': {
                    'logs': '/root/solbottrad/bot.log',
                    'data': '/root/solbottrad/data/'
                }
            }
        
        with open(project_dir / "config.yaml", 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        return {
            'success': True,
            'project_dir': str(project_dir),
            'agents': agents,
            'system_state': str(project_dir / "shared-knowledge" / "SYSTEM_STATE.md")
        }
    
    def get_project_state(self, project_name):
        """Read current project state"""
        project_dir = self.projects_dir / project_name
        
        if not project_dir.exists():
            return None
        
        state_file = project_dir / "shared-knowledge" / "SYSTEM_STATE.md"
        config_file = project_dir / "config.yaml"
        
        state = {
            'name': project_name,
            'path': str(project_dir),
            'exists': True
        }
        
        if state_file.exists():
            state['system_state'] = state_file.read_text()
        
        if config_file.exists():
            with open(config_file) as f:
                state['config'] = yaml.safe_load(f)
        
        return state

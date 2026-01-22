"""Orchestrate command - AI dev team coordination"""
import click
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.orchestrator.project_manager import ProjectManager
from core.orchestrator.task_manager import TaskManager

@click.command()
@click.argument('project_name')
@click.option('--goal', required=True, help='Project goal/objective')
@click.option('--agents', default='gemini,claude,grok,claude-code', help='AI agents to use')
@click.option('--based-on', default=None, help='Base on existing project')
def orchestrate(project_name, goal, agents, based_on):
    """Create and orchestrate new AI dev project"""
    
    click.echo(f"🎼 Orchestrating AI dev team for: {project_name}")
    click.echo("")
    
    # Parse agents
    agent_list = [a.strip() for a in agents.split(',')]
    
    click.echo(f"📋 Configuration:")
    click.echo(f"   Goal: {goal}")
    click.echo(f"   AI Team: {', '.join(agent_list)}")
    if based_on:
        click.echo(f"   Based on: {based_on}")
    click.echo("")
    
    # Create project
    pm = ProjectManager()
    result = pm.create_project(project_name, goal, agent_list, based_on)
    
    if result['success']:
        click.echo("✅ Project initialized!")
        click.echo(f"   Location: {result['project_dir']}")
        click.echo(f"   System State: {result['system_state']}")
        click.echo("")
        
        click.echo("📁 Directory structure created:")
        click.echo(f"   ├─ shared-knowledge/")
        click.echo(f"   │  ├─ SYSTEM_STATE.md  ← All AIs read/write here")
        click.echo(f"   │  ├─ AI_TASKS.md")
        click.echo(f"   │  └─ decisions.json")
        click.echo(f"   ├─ data/")
        click.echo(f"   │  ├─ raw/")
        click.echo(f"   │  └─ analysis/")
        click.echo(f"   └─ config.yaml")
        click.echo("")
        
        # If based on existing project, sync data
        if based_on:
            click.echo("🔄 Next steps:")
            click.echo(f"   1. Sync data: ai-nexus sync {project_name}")
            click.echo(f"   2. Assign tasks: ai-nexus tasks assign {project_name}")
            click.echo(f"   3. Check consensus: ai-nexus consensus {project_name}")
        else:
            click.echo("🔄 Next steps:")
            click.echo(f"   1. Configure data sources in config.yaml")
            click.echo(f"   2. Assign tasks: ai-nexus tasks assign {project_name}")
        
    else:
        click.echo(f"❌ Failed to create project: {result.get('error')}")

@click.command()
@click.argument('project_name')
def status(project_name):
    """Show project orchestration status"""
    
    pm = ProjectManager()
    state = pm.get_project_state(project_name)
    
    if not state:
        click.echo(f"❌ Project '{project_name}' not found")
        return
    
    click.echo(f"📊 Project Status: {project_name}")
    click.echo(f"   Location: {state['path']}")
    click.echo("")
    
    if 'config' in state:
        config = state['config']
        click.echo("🤖 AI Agents:")
        for agent, info in config.get('agents', {}).items():
            status_icon = "✅" if info.get('enabled') else "⚠️"
            click.echo(f"   {status_icon} {agent}: {info.get('status', 'unknown')}")
        click.echo("")
    
    # Check for tasks
    tm = TaskManager(project_name)
    tasks = tm.get_all_tasks()
    pending = [t for t in tasks.values() if t['status'] == 'pending']
    completed = [t for t in tasks.values() if t['status'] == 'completed']
    
    click.echo("📋 Tasks:")
    click.echo(f"   Pending: {len(pending)}")
    click.echo(f"   Completed: {len(completed)}")
    click.echo("")
    
    click.echo("📄 View full state:")
    system_state = Path(state['path']) / "shared-knowledge" / "SYSTEM_STATE.md"
    if system_state.exists():
        click.echo(f"   cat {system_state}")

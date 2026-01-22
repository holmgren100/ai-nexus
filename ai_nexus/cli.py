#!/usr/bin/env python3
import click
from .version import VERSION

@click.group()
@click.version_option(version=VERSION)
def main():
    """ai-nexus - Universal AI Collaboration Platform"""
    pass

@main.command()
def status():
    """Show platform status"""
    click.echo("🎯 ai-nexus platform status:")
    click.echo(f"  Version: {VERSION}")
    click.echo(f"  Status: ✅ Installed")

@main.command()
@click.argument('project_name')
def init(project_name):
    """Initialize a new project"""
    click.echo(f"🚀 Initializing project: {project_name}")
    click.echo("  Creating project structure...")
    
    from pathlib import Path
    project_dir = Path.home() / "ai-nexus" / "projects" / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (project_dir / "data" / "logs").mkdir(parents=True, exist_ok=True)
    (project_dir / "data" / "ml-data").mkdir(parents=True, exist_ok=True)
    (project_dir / "data" / "code").mkdir(parents=True, exist_ok=True)
    
    click.echo(f"  ✅ Project {project_name} initialized!")
    click.echo(f"  📁 Location: {project_dir}")

@main.command()
@click.argument('project_name')
def sync(project_name):
    """Sync data from spoke server"""
    from .commands.sync import sync as sync_cmd
    ctx = click.get_current_context()
    ctx.invoke(sync_cmd, project_name=project_name)

if __name__ == '__main__':
    main()

@main.command()
@click.argument('project_name')
def setup_cron(project_name):
    """Setup automatic hourly sync for project"""
    import subprocess
    from pathlib import Path
    
    script = Path(__file__).parent.parent / "scripts" / "setup_cron.sh"
    result = subprocess.run([str(script), project_name], capture_output=True, text=True)
    
    click.echo(result.stdout)
    if result.returncode != 0:
        click.echo(result.stderr)

@main.command()
@click.argument('project_name')
@click.argument('question')
def ask(project_name, question):
    """Ask AI agents about project"""
    from .commands.ask import ask as ask_cmd
    ctx = click.get_current_context()
    ctx.invoke(ask_cmd, project_name=project_name, question=question)

@main.command()
@click.argument('project_name')
def analyze(project_name):
    """Analyze project data locally"""
    from .commands.analyze import analyze as analyze_cmd
    ctx = click.get_current_context()
    ctx.invoke(analyze_cmd, project_name=project_name)

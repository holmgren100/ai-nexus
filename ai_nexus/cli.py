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
    click.echo(f"  ✅ Project {project_name} initialized!")

if __name__ == '__main__':
    main()

"""Sync command - syncs data from spoke servers"""
import click
import yaml
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.collectors.remote_collector import RemoteCollector

@click.command()
@click.argument('project_name')
def sync(project_name):
    """Sync data from spoke server for a project"""
    
    click.echo(f"🔄 Syncing project: {project_name}")
    
    # For now, hardcoded config for solana-bot
    # Later: read from config file
    if project_name == "solana-bot":
        config = {
            'host': '209.38.229.243',
            'user': 'root',
            'ssh_key': '~/.ssh/id_ai_nexus',
            'paths': {
                'logs': '/root/solbottrad/bot.log',
                'data': '/root/solbottrad/data/',
                'code': '/root/solbottrad/trading_bot/'
            }
        }
    else:
        click.echo(f"❌ Project {project_name} not configured yet")
        return
    
    # Create collector
    collector = RemoteCollector(
        host=config['host'],
        user=config['user'],
        ssh_key=config['ssh_key'],
        paths=config['paths']
    )
    
    # Test connection
    click.echo("  Testing connection...")
    success, result = collector.test_connection()
    if not success:
        click.echo(f"  ❌ Connection failed: {result}")
        return
    click.echo(f"  ✅ Connected to: {result}")
    
    # Check bot status
    click.echo("  Checking bot status...")
    active, status = collector.get_bot_status()
    if active:
        click.echo(f"  ✅ Trading bot: {status}")
    else:
        click.echo(f"  ⚠️  Trading bot: {status}")
    
    # Sync logs
    click.echo("  Syncing logs...")
    local_logs = Path.home() / "ai-nexus" / "projects" / project_name / "data" / "logs"
    success, result = collector.sync_logs(local_logs)
    if success:
        click.echo(f"  ✅ Logs: {result}")
    else:
        click.echo(f"  ❌ Logs failed: {result}")
    
    # Sync data
    click.echo("  Syncing ML data...")
    local_data = Path.home() / "ai-nexus" / "projects" / project_name / "data" / "ml-data"
    success, result = collector.sync_data(local_data)
    if success:
        click.echo(f"  ✅ Data: {result}")
    else:
        click.echo(f"  ❌ Data failed: {result}")
    
    click.echo(f"🎉 Sync complete for {project_name}!")
    click.echo(f"📁 Data location: ~/ai-nexus/projects/{project_name}/data/")

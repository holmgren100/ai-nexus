"""Ask command - query AI agents about project"""
import click
from pathlib import Path
import json
import csv
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.ai_agents.gemini_agent import GeminiAgent

@click.command()
@click.argument('project_name')
@click.argument('question')
def ask(project_name, question):
    """Ask AI agents to analyze project data"""
    
    click.echo(f"🤖 Asking AI about: {project_name}")
    click.echo(f"❓ Question: {question}")
    click.echo("")
    
    # Get project data
    project_dir = Path.home() / "ai-nexus" / "projects" / project_name
    
    if not project_dir.exists():
        click.echo(f"❌ Project {project_name} not found. Run: ai-nexus init {project_name}")
        return
    
    # Gather context
    context = {}
    
    # Check for ML data
    ml_data_file = project_dir / "data" / "ml-data" / "ml_trades.csv"
    if ml_data_file.exists():
        try:
            with open(ml_data_file, 'r') as f:
                reader = csv.DictReader(f)
                trades = list(reader)
                context['total_trades'] = len(trades)
                context['sample_trades'] = trades[:5] if trades else []
        except Exception as e:
            context['ml_data_error'] = str(e)
    
    # Check for trade history
    history_file = project_dir / "data" / "ml-data" / "trade_history_all.csv"
    if history_file.exists():
        try:
            with open(history_file, 'r') as f:
                reader = csv.DictReader(f)
                history = list(reader)
                context['trade_history_count'] = len(history)
        except Exception as e:
            context['history_error'] = str(e)
    
    # Check logs
    log_file = project_dir / "data" / "logs" / "bot.log"
    if log_file.exists():
        context['log_size_mb'] = log_file.stat().st_size / (1024 * 1024)
    
    click.echo("📊 Context gathered:")
    click.echo(f"  ML trades: {context.get('total_trades', 0)}")
    click.echo(f"  Trade history: {context.get('trade_history_count', 0)}")
    click.echo(f"  Log size: {context.get('log_size_mb', 0):.1f} MB")
    click.echo("")
    
    # Use Gemini agent
    click.echo("🧠 Querying Gemini AI...")
    agent = GeminiAgent(project_name)
    
    if not agent.is_configured():
        click.echo("⚠️  Gemini API key not configured!")
        click.echo("")
        click.echo("To use AI analysis:")
        click.echo("  1. Get API key: https://makersuite.google.com/app/apikey")
        click.echo("  2. Set environment variable:")
        click.echo("     export GEMINI_API_KEY='your-key-here'")
        click.echo("  3. Add to ~/.bashrc to persist")
        return
    
    result = agent.analyze(question, context)
    
    if result['success']:
        click.echo("")
        click.echo("=" * 60)
        click.echo(result['response'])
        click.echo("=" * 60)
    else:
        click.echo(f"❌ Error: {result['error']}")

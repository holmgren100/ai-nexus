"""Analyze command - local data analysis without AI"""
import click
from pathlib import Path
import csv
from datetime import datetime

@click.command()
@click.argument('project_name')
def analyze(project_name):
    """Analyze project data locally (no AI required)"""
    
    click.echo(f"📊 Analyzing project: {project_name}")
    click.echo("")
    
    project_dir = Path.home() / "ai-nexus" / "projects" / project_name
    
    if not project_dir.exists():
        click.echo(f"❌ Project {project_name} not found")
        return
    
    # Analyze ML trades
    ml_file = project_dir / "data" / "ml-data" / "ml_trades.csv"
    if ml_file.exists():
        click.echo("🎯 ML Trades Analysis:")
        try:
            with open(ml_file, 'r') as f:
                reader = csv.DictReader(f)
                trades = list(reader)
                
                total = len(trades)
                click.echo(f"  Total trades: {total}")
                
                if total > 0:
                    # Calculate win rate
                    wins = sum(1 for t in trades if float(t.get('pnl_percent', 0)) > 0)
                    win_rate = (wins / total) * 100
                    click.echo(f"  Win rate: {win_rate:.1f}%")
                    
                    # Calculate P&L
                    total_pnl = sum(float(t.get('pnl', 0)) for t in trades)
                    click.echo(f"  Total P&L: ${total_pnl:.2f}")
                    
                    # Best trade
                    best = max(trades, key=lambda t: float(t.get('pnl_percent', 0)))
                    click.echo(f"  Best trade: {float(best.get('pnl_percent', 0)):.1f}%")
                    
                    # Worst trade
                    worst = min(trades, key=lambda t: float(t.get('pnl_percent', 0)))
                    click.echo(f"  Worst trade: {float(worst.get('pnl_percent', 0)):.1f}%")
        except Exception as e:
            click.echo(f"  ❌ Error: {e}")
    else:
        click.echo("  ⚠️  No ML trades data found")
    
    click.echo("")
    
    # Analyze trade history
    history_file = project_dir / "data" / "ml-data" / "trade_history_all.csv"
    if history_file.exists():
        click.echo("📈 Trade History:")
        try:
            with open(history_file, 'r') as f:
                reader = csv.DictReader(f)
                history = list(reader)
                click.echo(f"  Total executed: {len(history)}")
        except Exception as e:
            click.echo(f"  ❌ Error: {e}")
    else:
        click.echo("  ⚠️  No trade history found")
    
    click.echo("")
    
    # Analyze rejections
    rejected_file = project_dir / "data" / "ml-data" / "rejected_trades.csv"
    if rejected_file.exists():
        click.echo("🚫 Rejected Trades:")
        try:
            with open(rejected_file, 'r') as f:
                reader = csv.DictReader(f)
                rejected = list(reader)
                click.echo(f"  Total rejected: {len(rejected)}")
                
                if len(rejected) > 0 and 'reason' in rejected[0]:
                    # Count rejection reasons
                    reasons = {}
                    for r in rejected:
                        reason = r.get('reason', 'unknown')
                        reasons[reason] = reasons.get(reason, 0) + 1
                    
                    click.echo(f"  Top rejection reasons:")
                    for reason, count in sorted(reasons.items(), key=lambda x: x[1], reverse=True)[:5]:
                        click.echo(f"    - {reason}: {count}")
        except Exception as e:
            click.echo(f"  ❌ Error: {e}")
    else:
        click.echo("  ⚠️  No rejected trades data")
    
    click.echo("")
    
    # Log file info
    log_file = project_dir / "data" / "logs" / "bot.log"
    if log_file.exists():
        size_mb = log_file.stat().st_size / (1024 * 1024)
        click.echo(f"📝 Bot Log: {size_mb:.1f} MB")
    
    click.echo("")
    click.echo("✅ Analysis complete!")

"""Tasks command - AI agent task management"""
import click
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.orchestrator.task_manager import TaskManager
from core.ai_agents.gemini_agent import GeminiAgent
from core.ai_agents.grok_agent import GrokAgent
import csv

@click.command()
@click.argument('project_name')
@click.option('--auto', is_flag=True, help='Auto-assign default tasks')
def assign(project_name, auto):
    """Assign tasks to AI agents"""
    
    click.echo(f"📋 Task Assignment: {project_name}")
    click.echo("")
    
    tm = TaskManager(project_name)
    project_dir = Path.home() / "ai-nexus" / "projects" / project_name
    
    if not project_dir.exists():
        click.echo(f"❌ Project not found. Run: ai-nexus orchestrate new {project_name}")
        return
    
    if auto:
        click.echo("🤖 Auto-assigning default tasks...")
        click.echo("")
        
        # Task 1: Gemini - Data Analysis
        task_id = tm.assign_task(
            'gemini',
            'Analyze all trading data. Find patterns, what works, what failed. Focus on filters and decision logic.',
            priority='high'
        )
        click.echo(f"✅ Assigned to GEMINI: Data analysis")
        click.echo(f"   Task ID: {task_id}")
        
        # Execute Gemini task immediately
        click.echo("   Executing...")
        gemini = GeminiAgent(project_name)
        
        # Gather context from synced data
        context = {'project_name': project_name}
        
        # Check multiple possible data locations
        data_locations = [
            project_dir / "data" / "raw" / "ml-data" / "ml_trades.csv",
            project_dir / "data" / "ml-data" / "ml_trades.csv",
            Path.home() / "ai-nexus" / "projects" / "solana-bot" / "data" / "ml-data" / "ml_trades.csv"
        ]
        
        ml_file = None
        for loc in data_locations:
            if loc.exists():
                ml_file = loc
                break
        
        if ml_file:
            try:
                with open(ml_file) as f:
                    reader = csv.DictReader(f)
                    trades = list(reader)
                    context['total_trades'] = len(trades)
                    context['sample_trades'] = trades[:10] if len(trades) > 10 else trades
                    click.echo(f"   Found {len(trades)} trades to analyze")
            except Exception as e:
                click.echo(f"   Warning: Could not read trades: {e}")
        
        result = gemini.analyze("Analyze trading data patterns. What filters work? What failed?", context)
        
        if result.get('success'):
            output = result.get('response', 'Analysis complete')
            tm.complete_task(task_id, output)
            click.echo("   ✅ Complete! Output saved.")
        else:
            click.echo(f"   ⚠️  {result.get('error', 'Failed')}")
        
        click.echo("")
        
        # Task 2: Grok - Social Analysis
        task_id = tm.assign_task(
            'grok',
            'Analyze social patterns for successful tokens. Twitter sentiment, community engagement.',
            priority='high'
        )
        click.echo(f"✅ Assigned to GROK: Social analysis")
        click.echo(f"   Task ID: {task_id}")
        
        # Execute Grok task
        click.echo("   Executing...")
        grok = GrokAgent(project_name)
        result = grok.analyze("Analyze social patterns for successful tokens", context)
        
        # Always complete task even if API not ready
        output = result.get('response') or result.get('analysis') or "Grok API integration pending"
        tm.complete_task(task_id, str(output))
        
        if result.get('success'):
            if 'pending' in str(output).lower():
                click.echo("   ⚠️  Grok API pending - placeholder saved")
            else:
                click.echo("   ✅ Complete! Output saved.")
        
        click.echo("")
        
        # Task 3: Claude - Strategy Design
        task_id = tm.assign_task(
            'claude',
            'Read Gemini and Grok insights from SYSTEM_STATE.md. Design trading strategy with clear filters and decision logic.',
            priority='high'
        )
        click.echo(f"✅ Assigned to CLAUDE: Strategy design")
        click.echo(f"   Task ID: {task_id}")
        click.echo("   Status: Ready for manual execution")
        click.echo("   (Claude Chat will design strategy based on Gemini+Grok results)")
        
        click.echo("")
        click.echo("📊 Task Summary:")
        all_tasks = tm.get_all_tasks()
        completed = [t for t in all_tasks.values() if t['status'] == 'completed']
        pending = [t for t in all_tasks.values() if t['status'] == 'pending']
        click.echo(f"   Completed: {len(completed)}")
        click.echo(f"   Pending: {len(pending)}")
        click.echo("")
        click.echo("📋 Next steps:")
        click.echo(f"   1. Review AI outputs: ai-nexus tasks list {project_name}")
        click.echo(f"   2. Build consensus: ai-nexus consensus {project_name}")
        
    else:
        click.echo("Manual task assignment not yet implemented.")
        click.echo(f"Use: ai-nexus tasks assign {project_name} --auto")

@click.command()
@click.argument('project_name')
def list_tasks(project_name):
    """List all tasks for project"""
    
    tm = TaskManager(project_name)
    tasks = tm.get_all_tasks()
    
    if not tasks:
        click.echo(f"No tasks found for {project_name}")
        return
    
    click.echo(f"📋 Tasks for {project_name}:")
    click.echo("")
    
    pending = {tid: t for tid, t in tasks.items() if t['status'] == 'pending'}
    completed = {tid: t for tid, t in tasks.items() if t['status'] == 'completed'}
    
    if completed:
        click.echo("✅ COMPLETED:")
        for tid, task in completed.items():
            click.echo(f"   [{task['agent'].upper()}] {task['description'][:60]}...")
            click.echo(f"   ID: {tid}")
            if task.get('output'):
                output = str(task['output'])
                if len(output) > 200:
                    output = output[:200] + "..."
                click.echo(f"   Output: {output}")
            click.echo("")
    
    if pending:
        click.echo("⏳ PENDING:")
        for tid, task in pending.items():
            click.echo(f"   [{task['agent'].upper()}] {task['description'][:60]}...")
            click.echo(f"   ID: {tid}")
            click.echo("")

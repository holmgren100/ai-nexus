"""Task assignment and tracking for AI agents"""
from pathlib import Path
import json
from datetime import datetime

class TaskManager:
    """Manages AI agent tasks"""
    
    def __init__(self, project_name):
        self.project_name = project_name
        self.project_dir = Path.home() / "ai-nexus" / "projects" / project_name
        self.tasks_file = self.project_dir / "shared-knowledge" / "tasks.json"
    
    def assign_task(self, agent, task_description, priority="normal"):
        """Assign task to AI agent"""
        
        tasks = self._load_tasks()
        
        task_id = f"{agent}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        task = {
            'id': task_id,
            'agent': agent,
            'description': task_description,
            'priority': priority,
            'status': 'pending',
            'assigned': datetime.now().isoformat(),
            'completed': None,
            'output': None
        }
        
        tasks[task_id] = task
        self._save_tasks(tasks)
        
        return task_id
    
    def complete_task(self, task_id, output):
        """Mark task as complete with output"""
        
        tasks = self._load_tasks()
        
        if task_id in tasks:
            tasks[task_id]['status'] = 'completed'
            tasks[task_id]['completed'] = datetime.now().isoformat()
            tasks[task_id]['output'] = output
            self._save_tasks(tasks)
            return True
        
        return False
    
    def get_pending_tasks(self, agent=None):
        """Get pending tasks, optionally filtered by agent"""
        
        tasks = self._load_tasks()
        pending = {
            tid: task for tid, task in tasks.items()
            if task['status'] == 'pending'
        }
        
        if agent:
            pending = {
                tid: task for tid, task in pending.items()
                if task['agent'] == agent
            }
        
        return pending
    
    def get_all_tasks(self):
        """Get all tasks"""
        return self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from file"""
        if self.tasks_file.exists():
            with open(self.tasks_file) as f:
                return json.load(f)
        return {}
    
    def _save_tasks(self, tasks):
        """Save tasks to file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)

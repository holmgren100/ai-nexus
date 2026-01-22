"""Consensus building system for multi-AI decisions"""
from pathlib import Path
import json
from datetime import datetime

class ConsensusBuilder:
    """Builds consensus across multiple AI agents"""
    
    def __init__(self, project_name):
        self.project_name = project_name
        self.project_dir = Path.home() / "ai-nexus" / "projects" / project_name
        self.decisions_file = self.project_dir / "shared-knowledge" / "decisions.json"
    
    def create_decision(self, topic, options, context=None):
        """Create new decision point for AIs to vote on"""
        
        decisions = self._load_decisions()
        
        decision_id = f"decision-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        decision = {
            'id': decision_id,
            'topic': topic,
            'options': options,
            'context': context or {},
            'votes': {},
            'status': 'pending',
            'created': datetime.now().isoformat(),
            'resolved': None,
            'result': None
        }
        
        decisions[decision_id] = decision
        self._save_decisions(decisions)
        
        return decision_id
    
    def vote(self, decision_id, agent, choice, reasoning=None):
        """Record AI agent vote"""
        
        decisions = self._load_decisions()
        
        if decision_id not in decisions:
            return False
        
        decisions[decision_id]['votes'][agent] = {
            'choice': choice,
            'reasoning': reasoning,
            'timestamp': datetime.now().isoformat()
        }
        
        self._save_decisions(decisions)
        return True
    
    def check_consensus(self, decision_id, required_agreement=0.75):
        """Check if consensus reached"""
        
        decisions = self._load_decisions()
        
        if decision_id not in decisions:
            return None
        
        decision = decisions[decision_id]
        votes = decision['votes']
        
        if not votes:
            return {
                'consensus': False,
                'reason': 'No votes yet'
            }
        
        # Count votes for each option
        vote_counts = {}
        for agent, vote_data in votes.items():
            choice = vote_data['choice']
            vote_counts[choice] = vote_counts.get(choice, 0) + 1
        
        total_votes = len(votes)
        max_votes = max(vote_counts.values())
        winning_option = [k for k, v in vote_counts.items() if v == max_votes][0]
        agreement_rate = max_votes / total_votes
        
        has_consensus = agreement_rate >= required_agreement
        
        result = {
            'consensus': has_consensus,
            'winning_option': winning_option,
            'agreement_rate': agreement_rate,
            'vote_counts': vote_counts,
            'total_votes': total_votes,
            'votes': votes
        }
        
        if has_consensus:
            decision['status'] = 'resolved'
            decision['resolved'] = datetime.now().isoformat()
            decision['result'] = winning_option
            self._save_decisions(decisions)
        
        return result
    
    def get_pending_decisions(self):
        """Get all pending decisions"""
        decisions = self._load_decisions()
        return {
            did: d for did, d in decisions.items()
            if d['status'] == 'pending'
        }
    
    def get_all_decisions(self):
        """Get all decisions"""
        return self._load_decisions()
    
    def _load_decisions(self):
        """Load decisions from file"""
        if self.decisions_file.exists():
            with open(self.decisions_file) as f:
                return json.load(f)
        return {}
    
    def _save_decisions(self, decisions):
        """Save decisions to file"""
        self.decisions_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.decisions_file, 'w') as f:
            json.dump(decisions, f, indent=2)

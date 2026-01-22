"""Base AI agent class"""
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, project_name):
        self.project_name = project_name
    
    @abstractmethod
    def analyze(self, question, context):
        """Analyze and return insights"""
        pass
    
    @abstractmethod
    def is_configured(self):
        """Check if agent is properly configured"""
        pass

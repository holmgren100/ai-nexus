"""Gemini AI agent for data analysis"""
import os
import json
from .base_agent import BaseAgent

class GeminiAgent(BaseAgent):
    """Gemini AI for pattern detection and analysis"""
    
    def __init__(self, project_name):
        super().__init__(project_name)
        self.api_key = os.getenv('GEMINI_API_KEY')
    
    def is_configured(self):
        """Check if Gemini API key is set"""
        return self.api_key is not None
    
    def analyze(self, question, context):
        """Analyze using Gemini API"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Gemini API key not configured. Set GEMINI_API_KEY environment variable.'
            }
        
        try:
            # Use NEW google.genai package (not deprecated one)
            import google.genai as genai
            from google.genai import types
            
            client = genai.Client(api_key=self.api_key)
            
            # Build prompt
            prompt = f"""You are an AI trading analyst helping analyze a Solana trading bot.

Project: {self.project_name}
Question: {question}

Context:
{json.dumps(context, indent=2)}

Provide a concise, actionable analysis focusing on:
1. Key insights from the data
2. Patterns or anomalies
3. Specific recommendations
4. Risk factors

Keep response under 500 words."""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return {
                'success': True,
                'agent': 'gemini',
                'response': response.text
            }
            
        except ImportError:
            return {
                'success': False,
                'error': 'google-genai package not installed. Run: pip install google-genai'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Gemini API error: {str(e)}'
            }

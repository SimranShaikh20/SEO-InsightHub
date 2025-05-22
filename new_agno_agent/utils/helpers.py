from agno_agent import Agent

class Helpers(Agent):
    def __init__(self):
        super().__init__("Helpers")
    
    def validate_url(self, url):
        """Basic URL validation"""
        if not url.startswith(('http://', 'https://')):
            return False
        return True
    
    def format_keywords(self, keyword_str):
        """Process keyword input string"""
        return [kw.strip().lower() for kw in keyword_str.split(',') if kw.strip()]
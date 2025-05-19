# agents/base_agent.py
from agno.agent import Agent
from abc import ABC, abstractmethod

class BaseAgent(Agent, ABC):
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)
        
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass

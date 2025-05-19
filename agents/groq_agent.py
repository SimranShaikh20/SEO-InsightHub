import os
import requests
from agno.agent import Agent
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class GroqAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Groq AI Agent",
            description="Generates AI-powered SEO recommendations using Groq API"
        )
        self.api_key = os.getenv('GROQ_API_KEY')
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'
        
    async def execute(self, seo_summary: str) -> str:
        """Get SEO recommendations using Groq API with Agno framework"""
        self.logger.info("Generating SEO recommendations with Groq AI")
        
        try:
            await self.log_event("seo_recommendation_started", {
                "summary_length": len(seo_summary)
            })
            
            prompt = f"""
            You are an expert SEO consultant. Based on the following website SEO analysis, provide 5 actionable improvement recommendations:

            {seo_summary}

            Please format your response as:
            1. [Specific recommendation with clear action steps]
            2. [Specific recommendation with clear action steps]
            3. [Specific recommendation with clear action steps]
            4. [Specific recommendation with clear action steps]
            5. [Specific recommendation with clear action steps]

            Focus on high-impact, implementable changes that will improve search engine rankings.
            """
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            }
            
            json_data = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 600,
                "temperature": 0.7,
            }
            
            response = requests.post(self.api_url, headers=headers, json=json_data)
            response.raise_for_status()
            data = response.json()
            
            result = data['choices'][0]['message']['content'].strip()
            
            await self.log_event("seo_recommendation_completed", {
                "recommendations_generated": True,
                "response_length": len(result),
                "tokens_used": data.get('usage', {}).get('total_tokens', 0)
            })
            
            self.logger.info("Successfully generated SEO recommendations")
            return result
            
        except Exception as e:
            await self.log_event("seo_recommendation_failed", {
                "error": str(e)
            })
            self.logger.error(f"Failed to generate SEO recommendations: {str(e)}")
            return f"Error generating SEO recommendations: {str(e)}"

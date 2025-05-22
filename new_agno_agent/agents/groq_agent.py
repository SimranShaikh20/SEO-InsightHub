from agno_agent import Agent
import groq
import os
from utils.config import GROQ_API_KEY

class GroqAgent(Agent):
    def __init__(self):
        super().__init__("GroqAgent")
        self.client = groq.Client(api_key=GROQ_API_KEY)
    
    def get_seo_recommendations(self, user_data, competitor_data, keywords):
        prompt = self._build_prompt(user_data, competitor_data, keywords)
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=2000
            )
            
            response = chat_completion.choices[0].message.content
            return self._parse_response(response)
        except Exception as e:
            self.log_error(f"Error getting GROQ recommendations: {str(e)}")
            return {
                'quick_wins': ["Could not generate recommendations due to API error"],
                'detailed_analysis': "Please check your API key and try again."
            }
    
    def _build_prompt(self, user_data, competitor_data, keywords):
        prompt = f"""
        You are an expert SEO consultant analyzing a website and comparing it with competitors. 
        Provide actionable recommendations to improve the website's SEO performance.
        
        Website being analyzed: {user_data['domain']}
        Competitors: {', '.join([c['domain'] for c in competitor_data if c])}
        Target keywords: {', '.join(keywords) if keywords else 'Not specified'}
        
        Here's the analysis data:
        
        Website Title: {user_data['title']}
        Meta Description: {'Present' if user_data['meta_description'] else 'Missing'}
        H1 Headings: {len(user_data['headings']['h1'])}
        H2 Headings: {len(user_data['headings']['h2'])}
        Images: {len(user_data['images'])} total, {sum(1 for img in user_data['images'] if img['alt'])} with alt text
        Status Code: {user_data['status_code']}
        Load Time: {user_data['load_time']} seconds
        
        Please provide:
        1. Top 5 quick SEO improvement steps
        2. Detailed analysis of technical and content SEO issues
        3. Specific recommendations for improving keyword targeting
        4. Any other relevant suggestions
        
        Format your response with clear headings and bullet points for readability.
        """
        
        return prompt
    
    def _parse_response(self, response_text):
        # Simple parsing - can be enhanced based on actual response format
        sections = response_text.split("\n\n")
        quick_wins = []
        detailed = []
        
        for section in sections:
            if "quick" in section.lower() or "top 5" in section.lower():
                lines = section.split('\n')
                quick_wins = [line.strip() for line in lines if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '-', '*'))]
            else:
                detailed.append(section)
        
        return {
            'quick_wins': quick_wins[:5],
            'detailed_analysis': "\n\n".join(detailed)
        }
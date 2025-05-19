
from agno.agent import Agent
from .firecrawl_agent import FirecrawlAgent
from .exa_agent import ExaAgent
from .groq_agent import GroqAgent
from .pdf_agent import PDFAgent
import asyncio
import logging
class SEOAgentManager(Agent):
    def __init__(self):
        super().__init__(name="SEO InsightHub Agent Manager")
        
        # Initialize all agents
        self.firecrawl_agent = FirecrawlAgent()
        self.exa_agent = ExaAgent()
        self.groq_agent = GroqAgent()
        self.pdf_agent = PDFAgent()
        self.logger = logging.getLogger(__name__)

        # Store all agents for easy access
        self.agents = {
            'firecrawl': self.firecrawl_agent,
            'exa': self.exa_agent,
            'groq': self.groq_agent,
            'pdf': self.pdf_agent
        }
        # # Register agents
        # self.add_agent(self.firecrawl_agent)
        # self.add_agent(self.exa_agent)
        # self.add_agent(self.groq_agent)
        # self.add_agent(self.pdf_agent)
    
    async def run_full_seo_analysis(self, website_url: str, competitor_urls: list, keywords: list):
        """Run complete SEO analysis workflow"""
        self.logger.info("Starting full SEO analysis workflow")
        
        # Step 1: Crawl all websites
        all_urls = [website_url] + competitor_urls[:3]
        crawl_tasks = [self.firecrawl_agent.execute(url) for url in all_urls]
        crawl_results = await self.run_parallel(crawl_tasks)
        
        # Step 2: Analyze keywords
        keyword_trends = await self.exa_agent.execute(keywords)
        
        # Step 3: Generate summary for AI recommendations
        summary_text = self._create_seo_summary(crawl_results)
        
        # Step 4: Get AI recommendations
        seo_recommendations = await self.groq_agent.execute(summary_text)
        
        return {
            'crawl_results': crawl_results,
            'keyword_trends': keyword_trends,
            'seo_recommendations': seo_recommendations
        }
    
    async def run_parallel(self, tasks):
        """Run multiple tasks in parallel"""
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    def _create_seo_summary(self, crawl_results):
        """Create summary text from crawl results for AI analysis"""
        summary_text = ""
        for site in crawl_results:
            summary_text += f"Site: {site['url']}\n"
            if 'error' in site:
                summary_text += f"Error: {site['error']}\n"
            else:
                summary_text += f"Title: {site['title']}\n"
                summary_text += f"Meta: {site['meta_description']}\n"
                for htag, texts in site['headings'].items():
                    summary_text += f"{htag.upper()}: {', '.join(texts)}\n"
            summary_text += "\n"
        return summary_text
 
 
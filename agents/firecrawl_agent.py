
import requests
from bs4 import BeautifulSoup
from agno.agent import Agent
from typing import Dict, Any

class FirecrawlAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Firecrawl Agent",
            description="Crawls websites and extracts SEO metadata including title, meta description, and headings structure"
        )
    
    async def execute(self, url: str) -> Dict[str, Any]:
        """Fetch page HTML and extract SEO info using Agno framework"""
        self.logger.info(f"Starting to crawl website: {url}")
        
        try:
            # Log the crawling attempt
            await self.log_event("crawl_started", {"url": url})
            
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Extract title
            title = soup.title.string if soup.title else ''
            
            # Extract meta description
            meta_desc = ''
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag:
                meta_desc = meta_tag.get('content', '')

            # Extract headings (H1, H2, H3)
            headings = {}
            for i in range(1, 4):
                tags = soup.find_all(f'h{i}')
                headings[f'h{i}'] = [tag.get_text(strip=True) for tag in tags]

            result = {
                'url': url,
                'title': title,
                'meta_description': meta_desc,
                'headings': headings
            }
            
            # Log successful extraction
            await self.log_event("crawl_completed", {
                "url": url,
                "title_length": len(title),
                "meta_desc_length": len(meta_desc),
                "heading_counts": {k: len(v) for k, v in headings.items()}
            })
            
            self.logger.info(f"Successfully crawled {url}")
            return result
            
        except Exception as e:
            # Log error
            await self.log_event("crawl_failed", {
                "url": url,
                "error": str(e)
            })
            self.logger.error(f"Failed to crawl {url}: {str(e)}")
            return {'url': url, 'error': str(e)}
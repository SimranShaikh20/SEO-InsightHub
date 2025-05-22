from agno_agent import Agent
import pandas as pd
from urllib.parse import urlparse

class AnalysisAgent(Agent):
    def __init__(self):
        super().__init__("AnalysisAgent")
    
    def compare_seo(self, user_data, competitor_data, keywords):
        results = {
            'comparison_table': self._create_comparison_table(user_data, competitor_data),
            'keyword_analysis': self._analyze_keywords(user_data, competitor_data, keywords)
        }
        return results
    
    def _create_comparison_table(self, user_data, competitor_data):
        # Prepare data for comparison
        all_data = [user_data] + competitor_data
        rows = []
        
        for data in all_data:
            if not data:
                continue
                
            rows.append({
                'Website': data['domain'],
                'Title Length': len(data['title']) if data['title'] else 0,
                'Meta Description': bool(data['meta_description']),
                'H1 Count': len(data['headings']['h1']),
                'H2 Count': len(data['headings']['h2']),
                'Image Count': len(data['images']),
                'Images with Alt': sum(1 for img in data['images'] if img['alt']),
                'Internal Links': sum(1 for link in data['links'] if urlparse(link['href']).netloc == data['domain']),
                'External Links': sum(1 for link in data['links'] if urlparse(link['href']).netloc != data['domain']),
                'Status Code': data['status_code'],
                'Load Time (s)': data['load_time']
            })
        
        return pd.DataFrame(rows)
    
    def _analyze_keywords(self, user_data, competitor_data, keywords):
        if not keywords:
            return pd.DataFrame()
            
        analysis = []
        
        for keyword in keywords:
            keyword = keyword.lower()
            user_count = self._count_keyword_occurrences(user_data, keyword)
            competitor_counts = [self._count_keyword_occurrences(comp, keyword) for comp in competitor_data if comp]
            
            analysis.append({
                'Keyword': keyword,
                'Your Site': user_count,
                **{f'Competitor {i+1}': count for i, count in enumerate(competitor_counts)},
                'Average Competitor': sum(competitor_counts)/len(competitor_counts) if competitor_counts else 0
            })
        
        return pd.DataFrame(analysis)
    
    def _count_keyword_occurrences(self, site_data, keyword):
        if not site_data:
            return 0
            
        count = 0
        keyword = keyword.lower()
        
        # Check in title
        if site_data['title'] and keyword in site_data['title'].lower():
            count += 1
        
        # Check in meta description
        if site_data['meta_description'] and keyword in site_data['meta_description'].lower():
            count += 1
        
        # Check in headings
        for heading_level in site_data['headings']:
            for heading in site_data['headings'][heading_level]:
                if keyword in heading.lower():
                    count += 1
        
        return count
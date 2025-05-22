from agno_agent import Agent
from agents.crawler_agent import CrawlerAgent
from agents.analysis_agent import AnalysisAgent
from agents.groq_agent import GroqAgent
from agents.report_agent import ReportAgent
import streamlit as st

class SEOInsightHub(Agent):
    def __init__(self):
        super().__init__("SEOInsightHub")
        self.crawler = CrawlerAgent()
        self.analyzer = AnalysisAgent()
        self.groq = GroqAgent()
        self.reporter = ReportAgent()
        
    def run(self):
        st.set_page_config(page_title="SEO InsightHub", layout="wide")
        st.title("SEO InsightHub - Analyze, Compare, and Optimize")
        
        # Sidebar inputs
        with st.sidebar:
            st.header("Input Parameters")
            user_url = st.text_input("Your Website URL")
            competitor_urls = st.text_area("Competitor URLs (one per line)", help="Enter 2-3 competitor URLs")
            keywords = st.text_input("Relevant Keywords (comma separated)")
            analyze_button = st.button("Analyze SEO")
        
        if analyze_button:
            with st.spinner("Analyzing websites..."):
                # Process inputs
                competitor_list = [url.strip() for url in competitor_urls.split('\n') if url.strip()]
                keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
                
                # Crawl websites
                user_data = self.crawler.crawl_website(user_url)
                competitor_data = [self.crawler.crawl_website(url) for url in competitor_list]
                
                # Analyze SEO
                analysis_results = self.analyzer.compare_seo(user_data, competitor_data, keyword_list)
                
                # Get AI recommendations
                ai_recommendations = self.groq.get_seo_recommendations(
                    user_data=user_data,
                    competitor_data=competitor_data,
                    keywords=keyword_list
                )
                
                # Display results
                self.display_results(analysis_results, ai_recommendations)
                
                # Generate report
                pdf_report = self.reporter.generate_pdf(
                    analysis_results, 
                    ai_recommendations,
                    user_url,
                    competitor_list
                )
                
                # Download button
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_report,
                    file_name="seo_insighthub_report.pdf",
                    mime="application/pdf"
                )
    
    def display_results(self, analysis_results, ai_recommendations):
        st.header("SEO Analysis Results")
        
        # Display comparison table
        st.subheader("SEO Metrics Comparison")
        st.dataframe(analysis_results['comparison_table'])
        
        # Display keyword analysis
        st.subheader("Keyword Analysis")
        st.dataframe(analysis_results['keyword_analysis'])
        
        # Display AI recommendations
        st.subheader("AI-Powered SEO Recommendations")
        for i, rec in enumerate(ai_recommendations['quick_wins'], 1):
            st.markdown(f"{i}. {rec}")
        
        st.subheader("Detailed Recommendations")
        st.write(ai_recommendations['detailed_analysis'])

if __name__ == "__main__":
    app = SEOInsightHub()
    app.run()
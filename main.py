import streamlit as st
import asyncio
from agents.agent_manager import SEOAgentManager

# Initialize agent manager
@st.cache_resource
def get_agent_manager():
    return SEOAgentManager()

def main():
    st.set_page_config(
        page_title="SEO InsightHub",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 SEO InsightHub - AI-Powered Website Analysis")
    st.markdown("*Analyze, Compare, and Optimize Your Website with Agno Agents*")
    
    # Initialize agent manager
    agent_manager = get_agent_manager()
    
    # Sidebar inputs
    with st.sidebar:
        st.header("📊 Analysis Configuration")
        
        your_website = st.text_input(
            "🎯 Your Website URL",
            placeholder="https://your-website.com"
        )
        
        competitor_urls = st.text_area(
            "🏢 Competitor URLs",
            placeholder="https://competitor1.com\nhttps://competitor2.com",
            help="Enter one URL per line (max 3 competitors)"
        ).splitlines()
        
        keywords_input = st.text_input(
            "🔑 Target Keywords",
            placeholder="SEO, digital marketing, website optimization",
            help="Enter keywords separated by commas"
        )
        keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
        
        st.markdown("---")
        
        # Analysis button
        analyze_button = st.button(
            "🚀 Start SEO Analysis",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    if analyze_button:
        if not your_website or not competitor_urls or not keywords:
            st.error("⚠️ Please provide your website URL, at least one competitor URL, and target keywords.")
            return
        
        # Run analysis
        with st.spinner("🤖 Agno agents are analyzing your SEO..."):
            # Create an event loop for async operations
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Run the full SEO analysis
                results = loop.run_until_complete(
                    agent_manager.run_full_seo_analysis(
                        your_website, 
                        competitor_urls, 
                        keywords
                    )
                )
                
                # Display results
                display_results(results, agent_manager)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
            finally:
                loop.close()

def display_results(results, agent_manager):
    """Display analysis results in a structured format"""
    
    # SEO Comparison Results
    st.header("🔍 Website SEO Analysis")
    
    crawl_results = results['crawl_results']
    keyword_trends = results['keyword_trends']
    seo_recommendations = results['seo_recommendations']
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Site Comparison", "📈 Keyword Analysis", "🤖 AI Recommendations", "📄 Export Report"])
    
    with tab1:
        st.subheader("Website Comparison Dashboard")
        
        for i, site in enumerate(crawl_results):
            with st.expander(f"🌐 {site['url']}", expanded=(i == 0)):
                if 'error' in site:
                    st.error(f"❌ Failed to analyze: {site['error']}")
                    continue
                
                # Create metrics columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Title Length", f"{len(site['title'])} chars")
                    if len(site['title']) > 60:
                        st.warning("⚠️ Title too long (>60 chars)")
                    elif len(site['title']) < 30:
                        st.warning("⚠️ Title too short (<30 chars)")
                    else:
                        st.success("✅ Title length optimal")
                
                with col2:
                    st.metric("Meta Description Length", f"{len(site['meta_description'])} chars")
                    if len(site['meta_description']) > 160:
                        st.warning("⚠️ Meta description too long (>160 chars)")
                    elif len(site['meta_description']) < 120:
                        st.warning("⚠️ Meta description too short (<120 chars)")
                    else:
                        st.success("✅ Meta description length optimal")
                
                with col3:
                    h1_count = len(site['headings'].get('h1', []))
                    st.metric("H1 Tags", h1_count)
                    if h1_count == 1:
                        st.success("✅ Perfect H1 structure")
                    elif h1_count == 0:
                        st.error("❌ No H1 tag found")
                    else:
                        st.warning(f"⚠️ Multiple H1 tags ({h1_count})")
                
                # Display content
                st.text_area("Title", site['title'], disabled=True)
                st.text_area("Meta Description", site['meta_description'], disabled=True)
                
                # Headings structure
                st.write("**Heading Structure:**")
                for htag, texts in site['headings'].items():
                    if texts:
                        st.write(f"• **{htag.upper()}** ({len(texts)}): {', '.join(texts[:3])}{'...' if len(texts) > 3 else ''}")
    
    with tab2:
        st.subheader("Keyword Trends & Analysis")
        
        for keyword, data in keyword_trends.items():
            with st.expander(f"🔑 {keyword}"):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.metric("Monthly Search Volume", f"{data['search_volume']:,}")
                
                with col2:
                    st.write("**Related Search Queries:**")
                    for query in data['related_queries']:
                        st.write(f"• {query}")
    
    with tab3:
        st.subheader("AI-Powered SEO Recommendations")
        st.markdown(seo_recommendations)
    
    with tab4:
        st.subheader("Export Analysis Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate PDF Report", use_container_width=True):
                with st.spinner("Generating PDF report..."):
                    try:
                        # Create event loop for async PDF generation
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        filename = loop.run_until_complete(
                            agent_manager.pdf_agent.execute(crawl_results)
                        )
                        
                        # Provide download
                        with open(filename, "rb") as pdf_file:
                            st.download_button(
                                "📥 Download PDF Report",
                                pdf_file,
                                file_name=filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        st.success("✅ PDF report generated successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Failed to generate PDF: {str(e)}")
                    finally:
                        loop.close()
        
        with col2:
            st.info("🔄 More export formats coming soon!")

if __name__ == "__main__":
    main()

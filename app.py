import streamlit as st
from services.firecrawl_service import crawl_site
from services.exa_service import get_trending_keywords
from services.groq_service import get_seo_advice
from services.agno_agent import agno_agent_augment
from utils.pdf_generator import generate_pdf_report

st.set_page_config(page_title="SEO InsightHub", layout="wide")
st.title("SEO InsightHub 📊")

url = st.text_input("Enter Your Website URL")
competitors = st.text_area("Enter Competitor URLs (comma-separated)")
keywords = st.text_input("Enter Keywords Relevant to Your Business")

if st.button("Analyze SEO"):
    if url:
        # Crawl website and get structured site data (title, headings, meta)
        site_data = crawl_site(url)
        st.success("Website crawled successfully!")

        # Get trending keywords from input keywords
        trending_keywords = get_trending_keywords(keywords)
        st.subheader("Trending Keywords")
        st.write(trending_keywords)

        # Prepare a summary string for GROQ (still accepts string input)
        analysis_summary_str = f"Site title: {site_data.get('title', '')}\n\nHeadings: {site_data.get('headings', {})}\n\nMeta: {site_data.get('meta', {})}"

        # Get GROQ AI SEO advice using summary string
        groq_advice = get_seo_advice(analysis_summary_str)

        # Pass structured site_data dict to AGNO agent for deeper insight
        agno_output = agno_agent_augment(site_data)

        st.subheader("GROQ AI SEO Recommendations")
        st.markdown(groq_advice)

        st.subheader("AGNO Agent Insight")
        st.markdown(agno_output)

        # Generate PDF with structured site_data
        generate_pdf_report(site_data, trending_keywords, groq_advice, agno_output)

        # Provide download button for the generated PDF report
        with open("SEO_Report.pdf", "rb") as file:
            st.download_button("Download SEO Report", data=file, file_name="SEO_Report.pdf")

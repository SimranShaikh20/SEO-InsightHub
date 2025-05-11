import streamlit as st
from seo_utils import crawl_website, get_trending_keywords
from groq_agent import generate_seo_tips
from report_generator import create_pdf

st.set_page_config(page_title="SEO InsightHub", layout="wide")
st.title("🔍 SEO InsightHub – Analyze, Compare, and Optimize Your Website")

url = st.text_input("Enter your website URL")
competitors = st.text_area("Competitor URLs (comma-separated)", "")
keywords = st.text_input("Business-related keywords")

if st.button("Analyze SEO"):
    if url and keywords:
        with st.spinner("🔄 Crawling your website..."):
            crawl_data = crawl_website(url)

        if "error" in crawl_data:
            st.error("Crawling failed.")
        else:
            # Mock issues based on example
            issues = "• Title tag too long\n• Missing meta description\n• No image alt attributes"
            trends = get_trending_keywords(keywords)
            trend_summary = ", ".join(trends)

            st.subheader("🚀 AI SEO Recommendations")
            output = generate_seo_tips(issues, trend_summary)
            st.markdown(f"```\n{output}\n```")

            st.success("🎯 SEO Suggestions Generated!")

            if st.button("📥 Download Report as PDF"):
                filename = create_pdf(output)
                with open(filename, "rb") as file:
                    st.download_button("Download PDF", file, filename=filename)
    else:
        st.warning("Please enter both website URL and keywords.")
st.sidebar.header("About")
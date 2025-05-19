import streamlit as st
from agents.firecrawl_agent import crawl_website
from agents.exa_agent import get_keyword_trends
from agents.groq_agent import generate_seo_tips

st.set_page_config(page_title="SEO InsightHub", layout="wide")

st.title("SEO InsightHub – Analyze, Compare, and Optimize Your Business Website")

st.sidebar.header("Input Your Details")

# Inputs
user_website = st.sidebar.text_input("Your Website URL", "https://example.com")

competitor_1 = st.sidebar.text_input("Competitor URL 1", "https://competitor1.com")
competitor_2 = st.sidebar.text_input("Competitor URL 2", "https://competitor2.com")
competitor_3 = st.sidebar.text_input("Competitor URL 3 (Optional)", "")

competitor_urls = [url for url in [competitor_1, competitor_2, competitor_3] if url.strip() != ""]

keywords_input = st.sidebar.text_input("Relevant Business Keywords (comma separated)", "seo, marketing, local business")
keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

if st.sidebar.button("Analyze SEO"):

    with st.spinner("Crawling websites..."):
        user_seo = crawl_website(user_website)
        competitors_seo = [crawl_website(url) for url in competitor_urls]

    with st.spinner("Fetching keyword trends..."):
        keyword_trends = get_keyword_trends(keywords)

    # Show user website SEO summary
    st.subheader(f"SEO Analysis for Your Website: {user_website}")
    st.write(user_seo)

    # Show competitors SEO summaries side by side
    st.subheader("Competitors SEO Analysis")
    for idx, comp_seo in enumerate(competitors_seo, 1):
        st.markdown(f"**Competitor {idx}: {comp_seo['url']}**")
        st.write(comp_seo)

    # Show keyword trends
    st.subheader("Keyword Trends")
    for kw, trend_data in keyword_trends.items():
        st.markdown(f"**Keyword:** {kw}")
        st.write(trend_data)

    # Prepare summary text for GROQ AI tips
    summary_text = f"User website SEO data: {user_seo}\n\nCompetitors SEO data: {competitors_seo}\n\nKeyword trends: {keyword_trends}"

    with st.spinner("Generating AI SEO improvement tips..."):
        ai_tips = generate_seo_tips(summary_text)

    st.subheader("AI-Generated SEO Improvement Tips")
    st.write(ai_tips)

    # PDF Report generation can be added here later

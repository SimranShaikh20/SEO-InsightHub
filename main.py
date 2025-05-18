import streamlit as st
from scraper.page_scraper import scrape_page
from analyzer.keyword_analysis import analyze_keywords
from analyzer.seo_checks import check_title, check_meta_description, check_image_alts
from llm.content_rewriter import rewrite_text
from reporting.seo_scorecard import create_seo_scorecard
from config import *

st.set_page_config(page_title="SEO Analyzer & Optimizer", layout="wide")

st.title("🔍 SEO Analyzer & Optimizer")
url = st.text_input("Enter the page URL to analyze:")

if st.button("Run Analysis") and url:
    with st.spinner("Scraping and analyzing content..."):
        content = scrape_page(url)
        keywords = analyze_keywords(content['text'])
        new_meta = rewrite_text(content['meta_desc'], [kw for kw, _ in keywords])
        title_ok = check_title(content['title'])
        meta_ok = check_meta_description(content['meta_desc'])
        missing_alts = check_image_alts(content['images'])
        scorecard = create_seo_scorecard(content, keywords, new_meta)

    st.subheader("📊 SEO Scorecard")
    st.json(scorecard)

    st.subheader("💡 Suggestions")
    st.markdown(f"**Title Check** ✅: {title_ok}")
    st.markdown(f"**Meta Description Check** ✅: {meta_ok}")
    st.markdown(f"**Images Missing ALT Text:** {len(missing_alts)}")
    st.markdown("**Top Keywords:**")
    st.write(keywords)
    st.markdown("**Suggested Meta Description Rewrite (LLM):**")
    st.success(new_meta)

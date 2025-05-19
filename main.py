import streamlit as st
from agents.crawl_agent import crawl_website
from agents.keyword_agent import get_keyword_trends
from agents.groq_agent import get_seo_recommendations
from utils.pdf_generator import generate_pdf_report

def main():
    st.title("SEO InsightHub - Analyze, Compare, and Optimize Your Website")

    st.sidebar.header("Input Data")
    your_website = st.sidebar.text_input("Your Website URL")
    competitor_urls = st.sidebar.text_area("Competitor URLs (one per line)").splitlines()
    keywords_input = st.sidebar.text_input("Relevant Business Keywords (comma separated)")
    keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]

    if st.sidebar.button("Analyze SEO"):

        if not your_website or len(competitor_urls) == 0 or len(keywords) == 0:
            st.error("Please enter your website, at least one competitor URL, and keywords.")
            return

        st.info("Crawling websites...")
        sites = [your_website] + competitor_urls[:3]
        crawl_results = [crawl_website(url) for url in sites]

        st.info("Fetching keyword trends...")
        keyword_trends = get_keyword_trends(keywords)

        st.info("Generating AI SEO recommendations...")
        # Create summary text from crawl data for AI prompt
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

        seo_tips = get_seo_recommendations(summary_text)

        st.subheader("SEO Comparison Dashboard")
        for site in crawl_results:
            st.markdown(f"### Website: {site['url']}")
            if 'error' in site:
                st.error(f"Failed to crawl: {site['error']}")
                continue
            st.write(f"**Title:** {site['title']}")
            st.write(f"**Meta Description:** {site['meta_description']}")
            st.write("**Headings:**")
            for htag, texts in site['headings'].items():
                st.write(f"{htag.upper()}: {', '.join(texts)}")

        st.subheader("Keyword Trends")
        for kw, info in keyword_trends.items():
            st.write(f"Keyword: {kw}")
            st.write(f"Search Volume: {info['search_volume']}")
            st.write(f"Related Queries: {', '.join(info['related_queries'])}")

        st.subheader("AI SEO Improvement Tips")
        st.write(seo_tips)

        if st.button("Download PDF Report"):
            filename = generate_pdf_report(crawl_results)
            with open(filename, "rb") as f:
                st.download_button("Download SEO Report PDF", f, file_name=filename)

if __name__ == "__main__":
    main()

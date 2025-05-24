import streamlit as st
from agno.agent import Agent
from agno.models.groq.groq import GROQ

from agno.tools.firecrawl import FirecrawlTools
from agno.tools.exa import ExaTools
from agno.tools.reasoning import ReasoningTools

# 🗝️ API Keys
FIRECRAWL_API_KEY = ""
EXA_API_KEY = ""
GROQ_API_KEY = ""

# ✅ Use GROQ directly from agno.models.groq
groq_model = GROQ(id="mixtral-8x7b-32768", api_key=GROQ_API_KEY)

# 🤖 Agno Agent Setup
agent = Agent(
    model=groq_model,
    tools=[
        FirecrawlTools(
            api_key=FIRECRAWL_API_KEY,
            analyze_headings=True,
            analyze_meta=True,
            crawl_depth=2
        ),
        ExaTools(
            api_key=EXA_API_KEY,
            keyword_trends=True,
            competitor_ranking=True
        ),
        ReasoningTools(add_instructions=True),
    ],
    instructions=[
        "Generate a detailed SEO report with sections:",
        "1. Website SEO structure analysis",
        "2. Competitor SEO benchmarking",
        "3. Keyword trend analysis",
        "4. AI-powered SEO improvement tips",
        "Use tables for comparisons and clearly label each section with markdown headers.",
        "Provide actionable, non-technical advice suitable for small business owners.",
        "Include a motivational closing summary encouraging optimization.",
        "Output only the report in markdown format — no extra text.",
    ],
    markdown=True,
)

def build_prompt(main_url, competitor_urls, keywords):
    competitor_str = ", ".join(competitor_urls)
    keywords_str = ", ".join(keywords)
    return f"""
    Analyze the following for SEO InsightHub:
    - Website URL: {main_url}
    - Competitor URLs: {competitor_str}
    - Business Keywords: {keywords_str}
    """

# 🌐 Streamlit UI
st.set_page_config(page_title="SEO InsightHub", layout="wide")
st.title("🚀 SEO InsightHub — AI-powered SEO Audit and Optimization Tool")

st.sidebar.header("🔍 Input Details")
main_url = st.sidebar.text_input("Your Website URL", value="https://example-business.com")

competitors = st.sidebar.text_area(
    "Competitor URLs (comma separated)", 
    value="https://competitor1.com, https://competitor2.com"
)

keywords = st.sidebar.text_area(
    "Business Keywords (comma separated)", 
    value="local bakery, fresh bread, artisan pastries"
)

generate_btn = st.sidebar.button("🧠 Generate SEO Report")

if generate_btn:
    competitor_urls = [url.strip() for url in competitors.split(",") if url.strip()]
    keywords_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
    
    st.subheader("📄 SEO Insight Report")
    report_placeholder = st.empty()
    full_report = ""

    prompt = build_prompt(main_url, competitor_urls, keywords_list)

    for chunk in agent.stream_response(prompt, show_full_reasoning=True, stream_intermediate_steps=True):
        full_report += chunk
        report_placeholder.markdown(full_report)

    st.sidebar.success("✅ SEO report generated!")

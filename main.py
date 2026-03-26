import streamlit as st

st.set_page_config(page_title="Visibility Audit Suite", layout="wide")

st.title("AI Visibility Audit Suite")

# Global Settings in Sidebar
with st.sidebar:
    st.header("Global Settings")
    country = st.selectbox(
        "Target Country/Region",
        ["United Kingdom", "United States", "Canada", "Australia", "Germany", "France", "Other"],
        index=0
    )
    st.session_state['target_country'] = country
    st.info(f"Audit context set to: {country}")

st.markdown(f"""
Welcome to the Audit Suite. Your current target region is **{country}**.
Select a tool from the sidebar to begin.

- **Audit Tool**: Deep dive into brand perception, sentiment, and GEO scoring.
- **Discovery Tool**: Crawl your site, generate unbranded keywords, and measure Share of Voice.
""")

st.subheader("New Features Active:")
st.success("✅ **Competitor Share of Voice**: Track how often rivals appear.")
st.success("✅ **Sentiment Analysis**: Automated polarity detection (Positive/Neutral/Negative).")
st.success("✅ **GEO Scoring**: Generative Engine Optimisation score (1-10).")
st.success("✅ **Hallucination Monitoring**: Identification of factual inconsistencies.")

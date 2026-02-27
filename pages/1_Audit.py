import streamlit as st
from utils.llm_handler import query_llm
from utils.prompts import CATEGORIES, format_prompt

st.set_page_config(page_title="AI Visibility Audit", layout="wide")

## Sidebar - API Configuration
with st.sidebar:
    st.header("API Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")

st.title("AI Visibility Auditor")

## Inputs
col1, col2 = st.columns([1, 2])
with col1:
    client_name = st.text_input("Client Name", placeholder="e.g. Acme Corp")
    competitor_input = st.text_area("Competitors (1 per line, max 3)", placeholder="Competitor A\nCompetitor B")
    competitors = [c.strip() for c in competitor_input.split('\n') if c.strip()][:3]

with col2:
    st.subheader("Audit Categories")
    selected_cats = [cat for cat in CATEGORIES.keys() if st.checkbox(cat)]

## Execution
if st.button("Run Audit"):
    if not (openai_key or gemini_key):
        st.error("Please provide at least one API key.")
    elif not client_name:
        st.error("Please provide a client name.")
    elif not selected_cats:
        st.warning("Please select at least one category.")
    else:
        results = {}
        providers = []
        if openai_key: providers.append(("OpenAI", openai_key))
        if gemini_key: providers.append(("Gemini", gemini_key))

        for cat in selected_cats:
            st.header(f"Results: {cat}")
            for question_template in CATEGORIES[cat]:
                prompt = format_prompt(question_template, client_name, competitors)
                st.subheader(f"Q: {question_template.replace('{client}', client_name)}")
                
                cols = st.columns(len(providers))
                for i, (p_name, p_key) in enumerate(providers):
                    with cols[i]:
                        with st.spinner(f"Querying {p_name}..."):
                            answer = query_llm(p_name, p_key, prompt)
                            st.markdown(f"**{p_name} Response:**")
                            st.info(answer)

import streamlit as st
import csv
import io
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
        results_for_csv = []
        providers = []
        if openai_key: providers.append(("OpenAI", openai_key))
        if gemini_key: providers.append(("Gemini", gemini_key))

        for cat in selected_cats:
            st.header(f"Results: {cat}")
            for q_data in CATEGORIES[cat]:
                question_template = q_data["question"]
                display_q = format_prompt(question_template, client_name, competitors)
                
                st.subheader(f"Q: {display_q}")
                st.caption(f"**Target Audience:** {q_data['audience']} | **Stage:** {q_data['funnel']}")
                st.info(f"*Goal: {q_data['goal']}*")
                
                cols = st.columns(len(providers))
                for i, (p_name, p_key) in enumerate(providers):
                    with cols[i]:
                        with st.spinner(f"Querying {p_name}..."):
                            answer = query_llm(p_name, p_key, display_q)
                            st.markdown(f"**{p_name} Response:**")
                            st.write(answer)
                            
                            # Collect for CSV
                            results_for_csv.append({
                                "Category": cat,
                                "Funnel Stage": q_data["funnel"],
                                "Audience": q_data["audience"],
                                "Question": display_q,
                                "Goal": q_data["goal"],
                                "Provider": p_name,
                                "Response": answer
                            })
        
        # Download button
        if results_for_csv:
            st.divider()
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["Category", "Funnel Stage", "Audience", "Question", "Goal", "Provider", "Response"])
            writer.writeheader()
            writer.writerows(results_for_csv)
            
            st.download_button(
                label="Download Results CSV",
                data=output.getvalue(),
                file_name=f"audit_results_{client_name.replace(' ', '_').lower()}.csv",
                mime="text/csv"
            )

import streamlit as st
import csv
import io
from concurrent.futures import ThreadPoolExecutor
from utils.llm_handler import query_llm
from utils.prompts import CATEGORIES, format_prompt
from utils.analysis import analyze_response, calculate_sov

st.set_page_config(page_title="AI Visibility Audit", layout="wide")

# Ensure session state exists
if 'target_country' not in st.session_state:
    st.session_state['target_country'] = "United Kingdom"

## Sidebar - API Configuration
with st.sidebar:
    st.header("API Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    st.info(f"Target Region: {st.session_state['target_country']}")

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

def run_query(p_name, p_key, prompt, q_metadata, cat, client_name, competitors, country):
    # Regional context injection
    regional_prompt = f"Context: User is in {country}. Question: {prompt}"
    answer = query_llm(p_name, p_key, regional_prompt)
    
    # Run analysis
    analysis = analyze_response(p_name, p_key, answer, client_name, country)
    sov = calculate_sov(answer, client_name, competitors)
    
    return {
        "Category": cat,
        "Funnel Stage": q_metadata["funnel"],
        "Audience": q_metadata["audience"],
        "Question": prompt,
        "Goal": q_metadata["goal"],
        "Provider": p_name,
        "Response": answer,
        "Sentiment": analysis.get("Sentiment", "Neutral"),
        "GEO Score": analysis.get("GEO Score", "5"),
        "Hallucination Risk": analysis.get("Hallucination Risk", "Low"),
        "Entities": analysis.get("Entities", ""),
        "Client Mentioned": "Yes" if sov.get(client_name) else "No",
        "Competitor Mentions": ", ".join([c for c in competitors if sov.get(c)])
    }

## Execution
if st.button("Run Audit"):
    if not (openai_key or gemini_key):
        st.error("Please provide at least one API key.")
    elif not client_name:
        st.error("Please provide a client name.")
    elif not selected_cats:
        st.warning("Please select at least one category.")
    else:
        providers = []
        if openai_key: providers.append(("OpenAI", openai_key))
        if gemini_key: providers.append(("Gemini", gemini_key))

        all_tasks = []
        for cat in selected_cats:
            for q_data in CATEGORIES[cat]:
                display_q = format_prompt(q_data["question"], client_name, competitors)
                for p_name, p_key in providers:
                    all_tasks.append((p_name, p_key, display_q, q_data, cat, client_name, competitors, st.session_state['target_country']))

        results_for_csv = []
        
        st.info(f"Running {len(all_tasks)} parallel queries with full analysis...")
        progress_bar = st.progress(0)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(run_query, *task) for task in all_tasks]
            for i, future in enumerate(futures):
                try:
                    res = future.result()
                    results_for_csv.append(res)
                except Exception as e:
                    st.error(f"Error in query: {e}")
                progress_bar.progress((i + 1) / len(all_tasks))

        # Group and display results
        for cat in selected_cats:
            st.header(f"Results: {cat}")
            cat_results = [r for r in results_for_csv if r["Category"] == cat]
            
            # Get unique questions in this category
            questions = list(dict.fromkeys([r["Question"] for r in cat_results]))
            
            for q_text in questions:
                q_res = [r for r in cat_results if r["Question"] == q_text]
                st.subheader(f"Q: {q_text}")
                st.caption(f"**Audience:** {q_res[0]['Audience']} | **Stage:** {q_res[0]['Funnel Stage']}")
                
                cols = st.columns(len(providers))
                for i, p_info in enumerate(providers):
                    p_name = p_info[0]
                    with cols[i]:
                        r = next((res for res in q_res if res["Provider"] == p_name), None)
                        if r:
                            st.markdown(f"**{p_name} Insights:**")
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Sentiment", r["Sentiment"])
                            c2.metric("GEO Score", r["GEO Score"])
                            c3.metric("Hallucination", r["Hallucination Risk"])
                            
                            with st.expander("View Full Response"):
                                st.write(r["Response"])
                                if r["Competitor Mentions"]:
                                    st.warning(f"Competitors mentioned: {r['Competitor Mentions']}")

        # Download button
        if results_for_csv:
            st.divider()
            output = io.StringIO()
            fieldnames = ["Category", "Funnel Stage", "Audience", "Question", "Goal", "Provider", "Response", "Sentiment", "GEO Score", "Hallucination Risk", "Entities", "Client Mentioned", "Competitor Mentions"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results_for_csv)
            
            st.download_button(
                label="Download Results CSV",
                data=output.getvalue(),
                file_name=f"audit_results_{client_name.replace(' ', '_').lower()}.csv",
                mime="text/csv"
            )

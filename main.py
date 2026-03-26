import streamlit as st
import csv
import io
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from utils.llm_handler import query_llm
from utils.prompts import BRANDED_CATEGORIES, UNBRANDED_CATEGORIES, format_prompt
from utils.analysis import analyze_response, calculate_sov

st.set_page_config(page_title="AI Visibility Audit Suite", layout="wide")

# Helper for crawling
def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        domain = urlparse(url).netloc
        for a in soup.find_all('a', href=True):
            link = urljoin(url, a['href'])
            if urlparse(link).netloc == domain:
                links.add(link)
        return list(links), soup.get_text()
    except: return [], ""

## Sidebar - API & Global Settings
with st.sidebar:
    st.header("Global Settings")
    openai_key = st.text_input("OpenAI API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    
    country = st.selectbox(
        "Target Country/Region",
        ["United Kingdom", "United States", "Canada", "Australia", "Germany", "France", "Other"],
        index=0
    )
    st.session_state['target_country'] = country

st.title("AI Visibility & Discovery Audit Suite")

## Shared Inputs
col1, col2 = st.columns([1, 1])
with col1:
    client_name = st.text_input("Client Name", placeholder="e.g. Acme Corp")
    website_url = st.text_input("Website URL", placeholder="https://www.acme.com")
    
    # Automatic Industry Detection
    industry_guess = "financial services"
    service_guess = "wealth management"
    
    if website_url and (openai_key or gemini_key):
        if 'last_url' not in st.session_state or st.session_state['last_url'] != website_url:
            with st.spinner("Analyzing website for industry context..."):
                _, text = get_links(website_url)
                p_name = "OpenAI" if openai_key else "Gemini"
                p_key = openai_key if openai_key else gemini_key
                prompt = f"Based on this text, what is the specific industry and the primary core service? Return as 'Industry | Service':\n\n{text[:2000]}"
                try:
                    res = query_llm(p_name, p_key, prompt)
                    if "|" in res:
                        industry_guess, service_guess = [x.strip() for x in res.split("|", 1)]
                        st.session_state['industry'] = industry_guess
                        st.session_state['service'] = service_guess
                        st.session_state['last_url'] = website_url
                except: pass

    industry = st.text_input("Industry", value=st.session_state.get('industry', industry_guess))
    core_service = st.text_input("Core Service", value=st.session_state.get('service', service_guess))

with col2:
    competitor_input = st.text_area("Competitors (1 per line, max 3)", placeholder="Competitor A\nCompetitor B")
    competitors = [c.strip() for c in competitor_input.split('\n') if c.strip()][:3]

tab1, tab2 = st.tabs(["Brand Audit", "Unbranded Audit"])

# --- Shared Query Function ---
def run_audit_query(p_name, p_key, prompt, q_metadata, cat, client, comps, country, is_branded=True):
    regional_prompt = f"Context: User is in {country}. Question: {prompt}"
    answer = query_llm(p_name, p_key, regional_prompt)
    analysis = analyze_response(p_name, p_key, answer, client, country)
    sov = calculate_sov(answer, client, comps)
    
    return {
        "Category": cat,
        "Funnel Stage": q_metadata.get("funnel", "N/A"),
        "Audience": q_metadata.get("audience", "General"),
        "Question": prompt,
        "Goal": q_metadata.get("goal", "N/A"),
        "Provider": p_name,
        "Response": answer,
        "Sentiment": analysis.get("Sentiment", "Neutral"),
        "GEO Score": analysis.get("GEO Score", "5"),
        "Hallucination Risk": analysis.get("Hallucination Risk", "Low"),
        "Client Mentioned": "Yes" if sov.get(client) else "No",
        "Competitor Mentions": ", ".join([c for c in comps if sov.get(c)])
    }

# --- Tab 1: Brand Audit ---
with tab1:
    st.header("Brand Perception Audit")
    st.markdown("Query LLMs using questions that specifically mention your brand.")
    
    selected_cats = [cat for cat in BRANDED_CATEGORIES.keys() if st.checkbox(cat, key=f"branded_cat_{cat}")]
    
    custom_questions_input = st.text_area("Add Custom Branded Questions (1 per line)", placeholder="How does {client} handle {industry} regulations?")
    custom_questions = [q.strip() for q in custom_questions_input.split('\n') if q.strip()]

    if st.button("Run Brand Audit"):
        if not (openai_key or gemini_key):
            st.error("Please provide at least one API key.")
        elif not client_name:
            st.error("Please provide a client name.")
        else:
            providers = []
            if openai_key: providers.append(("OpenAI", openai_key))
            if gemini_key: providers.append(("Gemini", gemini_key))

            all_tasks = []
            for cat in selected_cats:
                for q_data in BRANDED_CATEGORIES[cat]:
                    display_q = format_prompt(q_data["question"], client_name, competitors, country, industry, core_service)
                    for p_name, p_key in providers:
                        all_tasks.append((p_name, p_key, display_q, q_data, cat, client_name, competitors, country))
            
            for cq in custom_questions:
                display_q = cq.replace("{client}", client_name).replace("{competitors}", ", ".join(competitors)).replace("{industry}", industry).replace("{service}", core_service)
                for p_name, p_key in providers:
                    all_tasks.append((p_name, p_key, display_q, {}, "Custom", client_name, competitors, country))

            if not all_tasks:
                st.warning("Please select a category or add custom questions.")
            else:
                results = []
                st.info(f"Running {len(all_tasks)} branded queries...")
                progress = st.progress(0)
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = [executor.submit(run_audit_query, *t) for t in all_tasks]
                    for i, f in enumerate(futures):
                        results.append(f.result())
                        progress.progress((i+1)/len(all_tasks))
                
                for res in results:
                    with st.expander(f"Q: {res['Question']} ({res['Provider']})"):
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Sentiment", res["Sentiment"])
                        c2.metric("GEO Score", res["GEO Score"])
                        c3.metric("Hallucination", res["Hallucination Risk"])
                        st.write(res["Response"])
                
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
                st.download_button("Download Brand Audit CSV", output.getvalue(), "brand_audit.csv", "text/csv")

# --- Tab 2: Unbranded Audit ---
with tab2:
    st.header("Unbranded Visibility Audit")
    st.markdown(f"Analyze visibility for **{industry}** using generic questions and keyword-based discovery.")
    
    st.subheader("1. Industry-Wide Questions")
    selected_unbranded_cats = [cat for cat in UNBRANDED_CATEGORIES.keys() if st.checkbox(f"Include {cat}", value=True, key=f"unbranded_cat_{cat}")]
    
    st.subheader("2. Keyword Discovery")
    manual_keywords = st.text_area("Manual Keywords (Optional, 1 per line)", placeholder="wealth management")

    def extract_keywords(text, p_name, p_key, country, industry):
        prompt = f"Context: {country}. Identify 5 unbranded SEO keywords related to {industry}. Return ONLY keywords, one per line:\n\n{text[:4000]}"
        response = query_llm(p_name, p_key, prompt)
        return [k.strip() for k in response.split('\n') if k.strip()][:5]

    def generate_discovery_questions(keyword, p_name, p_key, country, industry):
        prompt = f"Context: {country}, Industry: {industry}. Generate 3 unbranded questions about '{keyword}'. Return ONLY questions, one per line."
        response = query_llm(p_name, p_key, prompt)
        return [q.strip() for q in response.split('\n') if q.strip()][:3]

    if st.button("Run Unbranded Audit"):
        if not (openai_key or gemini_key):
            st.error("Please provide at least one API key.")
        elif not client_name:
            st.error("Please provide a client name.")
        else:
            p_name = "OpenAI" if openai_key else "Gemini"
            p_key = openai_key if openai_key else gemini_key
            providers = []
            if openai_key: providers.append(("OpenAI", openai_key))
            if gemini_key: providers.append(("Gemini", gemini_key))

            all_unbranded_results = []
            
            with st.status("Running Unbranded Audit...") as status:
                # Part A: Category Questions
                cat_tasks = []
                for cat in selected_unbranded_cats:
                    for q_data in UNBRANDED_CATEGORIES[cat]:
                        display_q = format_prompt(q_data["question"], client_name, competitors, country, industry, core_service)
                        for pn, pk in providers:
                            cat_tasks.append((pn, pk, display_q, q_data, cat, client_name, competitors, country))
                
                # Part B: Keyword Discovery
                status.update(label="Crawling and generating keywords...", state="running")
                links, home_text = get_links(website_url)
                combined_text = home_text
                for link in links[:3]:
                    _, sub_text = get_links(link)
                    combined_text += "\n" + sub_text
                
                if manual_keywords:
                    keywords = [k.strip() for k in manual_keywords.split('\n') if k.strip()]
                else:
                    keywords = extract_keywords(combined_text, p_name, p_key, country, industry)
                
                st.write(f"Discovery Keywords: {', '.join(keywords)}")
                
                for kw in keywords:
                    qs = generate_discovery_questions(kw, p_name, p_key, country, industry)
                    for q in qs:
                        for pn, pk in providers:
                            cat_tasks.append((pn, pk, q, {"goal": f"Discovery for {kw}"}, "Keyword Discovery", client_name, competitors, country))
                
                # Execute all unbranded tasks
                status.update(label=f"Querying LLMs for {len(cat_tasks)} unbranded questions...", state="running")
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = [executor.submit(run_audit_query, *t) for t in cat_tasks]
                    for f in futures:
                        all_unbranded_results.append(f.result())
                
                status.update(label="Complete!", state="complete")

            # Summary Chart
            mentions = sum(1 for r in all_unbranded_results if r["Client Mentioned"] == "Yes")
            st.metric("Natural Share of Voice (Unbranded)", f"{(mentions/len(all_unbranded_results))*100:.1f}%")
            
            sov_chart = {client_name: mentions}
            for c in competitors:
                sov_chart[c] = sum(1 for r in all_unbranded_results if c in r["Competitor Mentions"])
            st.bar_chart(sov_chart)

            for res in all_unbranded_results:
                with st.expander(f"Q: {res['Question']} ({res['Provider']})"):
                    if res["Client Mentioned"] == "Yes": st.success("Client naturally mentioned!")
                    elif res["Competitor Mentions"]: st.warning(f"Competitors mentioned: {res['Competitor Mentions']}")
                    st.write(res["Response"])

            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=all_unbranded_results[0].keys())
            writer.writeheader()
            writer.writerows(all_unbranded_results)
            st.download_button("Download Unbranded Audit CSV", output.getvalue(), "unbranded_audit.csv", "text/csv")

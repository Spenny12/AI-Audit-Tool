import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import io
import csv
from concurrent.futures import ThreadPoolExecutor
from utils.llm_handler import query_llm
from utils.analysis import analyze_response, calculate_sov

st.set_page_config(page_title="AI Discovery Audit", layout="wide")

# Ensure session state exists
if 'target_country' not in st.session_state:
    st.session_state['target_country'] = "United Kingdom"

## Sidebar - API Configuration
with st.sidebar:
    st.header("API Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password")
    gemini_key = st.text_input("Gemini API Key", type="password")
    st.info(f"Target Region: {st.session_state['target_country']}")

st.title("AI Discovery & Visibility Auditor")
st.markdown("""
This tool crawls a website to understand its core offerings, generates unbranded SEO keywords, 
and then queries LLMs to see if the client naturally appears in the results.
""")

## Inputs
col1, col2 = st.columns([1, 2])
with col1:
    client_name = st.text_input("Client Name", placeholder="e.g. Acme Corp")
    website_url = st.text_input("Website URL", placeholder="https://www.acme.com")
    competitor_input = st.text_area("Competitors (1 per line, max 3)", placeholder="Competitor A\nCompetitor B")
    competitors = [c.strip() for c in competitor_input.split('\n') if c.strip()][:3]
    manual_keywords = st.text_area("Manual Keywords (Optional, 1 per line)", placeholder="wealth management\nretirement planning")

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
    except Exception as e:
        st.error(f"Error crawling {url}: {e}")
        return [], ""

def extract_keywords(text, p_name, p_key, country):
    prompt = f"Context: {country}. Based on the following website text, identify 5 SEO-friendly keywords or short phrases that represent the core services or offerings for this region. Return ONLY the keywords, one per line:\n\n{text[:4000]}"
    response = query_llm(p_name, p_key, prompt)
    return [k.strip() for k in response.split('\n') if k.strip()][:5]

def generate_questions(keyword, p_name, p_key, country):
    prompt = f"Context: {country}. Generate 5 common, unbranded informational questions that a potential customer in this region might ask an AI about '{keyword}'. Do NOT mention any specific brands. Return ONLY the questions, one per line."
    response = query_llm(p_name, p_key, prompt)
    return [q.strip() for q in response.split('\n') if q.strip()][:5]

def check_visibility(p_name, p_key, question, keyword, client, competitors, country):
    regional_prompt = f"Context: User is in {country}. Question: {question}"
    answer = query_llm(p_name, p_key, regional_prompt)
    
    analysis = analyze_response(p_name, p_key, answer, client, country)
    sov = calculate_sov(answer, client, competitors)
    
    return {
        "Keyword": keyword,
        "Question": question,
        "Provider": p_name,
        "Response": answer,
        "Mentioned": "Yes" if sov.get(client) else "No",
        "Competitor Mentions": ", ".join([c for c in competitors if sov.get(c)]),
        "Sentiment": analysis.get("Sentiment", "Neutral"),
        "GEO Score": analysis.get("GEO Score", "5"),
        "Hallucination Risk": analysis.get("Hallucination Risk", "Low")
    }

if st.button("Run Discovery Audit"):
    if not (openai_key or gemini_key):
        st.error("Please provide at least one API key.")
    elif not client_name or not website_url:
        st.error("Please provide both Client Name and Website URL.")
    else:
        p_name = "OpenAI" if openai_key else "Gemini"
        p_key = openai_key if openai_key else gemini_key
        country = st.session_state['target_country']

        with st.status("Crawling website and analyzing...") as status:
            links, home_text = get_links(website_url)
            combined_text = home_text
            for link in links[:5]:
                _, sub_text = get_links(link)
                combined_text += "\n" + sub_text
            
            status.update(label="Extracting regional keywords...", state="running")
            if manual_keywords:
                keywords = [k.strip() for k in manual_keywords.split('\n') if k.strip()]
            else:
                keywords = extract_keywords(combined_text, p_name, p_key, country)
            
            st.write(f"Target Keywords: {', '.join(keywords)}")
            
            status.update(label="Generating regional questions...", state="running")
            keyword_questions = {}
            for kw in keywords:
                keyword_questions[kw] = generate_questions(kw, p_name, p_key, country)
            
            status.update(label="Querying LLMs & Analyzing responses...", state="running")
            
            all_results = []
            providers = []
            if openai_key: providers.append(("OpenAI", openai_key))
            if gemini_key: providers.append(("Gemini", gemini_key))

            tasks = []
            for kw, qs in keyword_questions.items():
                for q in qs:
                    for pn, pk in providers:
                        tasks.append((pn, pk, q, kw, client_name, competitors, country))

            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(check_visibility, *t) for t in tasks]
                for future in futures:
                    all_results.append(future.result())
            
            status.update(label="Audit Complete!", state="complete")

        # Display Results
        st.header("Discovery Results")
        
        # Summary Metrics
        mentions = sum(1 for r in all_results if r["Mentioned"] == "Yes")
        total = len(all_results)
        st.metric("Client Visibility Score", f"{(mentions/total)*100:.1f}%", f"{mentions} mentions out of {total} queries")

        # Competitor SOV Summary
        st.subheader("Share of Voice (Mentions)")
        sov_counts = {client_name: mentions}
        for comp in competitors:
            c_mentions = sum(1 for r in all_results if comp in r["Competitor Mentions"])
            sov_counts[comp] = c_mentions
        
        st.bar_chart(sov_counts)

        for kw in keywords:
            with st.expander(f"Keyword: {kw}"):
                kw_results = [r for r in all_results if r["Keyword"] == kw]
                for q in keyword_questions[kw]:
                    st.subheader(f"Q: {q}")
                    q_results = [r for r in kw_results if r["Question"] == q]
                    cols = st.columns(len(providers))
                    for i, r in enumerate(q_results):
                        with cols[i]:
                            st.write(f"**{r['Provider']}**")
                            c1, c2 = st.columns(2)
                            c1.metric("Sentiment", r["Sentiment"])
                            c2.metric("GEO Score", r["GEO Score"])
                            
                            if r["Mentioned"] == "Yes":
                                st.success("Client Mentioned!")
                            elif r["Competitor Mentions"]:
                                st.warning(f"Competitors Mentioned: {r['Competitor Mentions']}")
                            else:
                                st.error("No tracked brands mentioned")

        # CSV Export
        output = io.StringIO()
        fieldnames = ["Keyword", "Question", "Provider", "Mentioned", "Competitor Mentions", "Sentiment", "GEO Score", "Hallucination Risk", "Response"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
        st.download_button("Download Discovery CSV", output.getvalue(), "discovery_audit.csv", "text/csv")

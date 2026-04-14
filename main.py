import streamlit as st
import csv
import io
import json
import time
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.llm_handler import query_llm, OPENAI_MODELS, GEMINI_MODELS
from utils.prompts import BRANDED_CATEGORIES, UNBRANDED_CATEGORIES, format_prompt
from utils.analysis import analyze_response, calculate_sov

# ─────────────────────────────────────────────
# Page config & custom CSS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Visibility Audit Suite",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Base & Typography ─────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Hide default Streamlit chrome ────────── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Page background & global text ───────── */
.stApp {
    background: #111827;
    color: #f1f5f9;
}

/* Ensure all plain text is readable */
.stApp p, .stApp li, .stApp span, .stApp label,
.stApp .stMarkdown, .stApp .stText {
    color: #e2e8f0;
}

/* Headings */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #f8fafc;
}

/* Caption / helper text */
.stApp .stCaption, .stApp small {
    color: #94a3b8;
}

/* ── Sidebar ──────────────────────────────── */
[data-testid="stSidebar"] {
    background: #1a2133;
    border-right: 1px solid #2d3748;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #94a3b8 !important;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
}

/* ── Card ─────────────────────────────────── */
.card {
    background: #1a2133;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* ── Metric cards ─────────────────────────── */
[data-testid="stMetric"] {
    background: #1e2a3e;
    border: 1px solid #2d3748;
    border-radius: 10px;
    padding: 1rem 1.25rem;
}
[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 700;
    color: #f1f5f9 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    color: #94a3b8 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Sentiment badges ─────────────────────── */
.badge {
    display: inline-block;
    padding: 0.2em 0.65em;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-positive  { background: #14532d; color: #bbf7d0; }
.badge-neutral   { background: #1e3a5f; color: #bae6fd; }
.badge-negative  { background: #450a0a; color: #fecaca; }
.badge-low       { background: #14532d; color: #bbf7d0; }
.badge-medium    { background: #78350f; color: #fde68a; }
.badge-high      { background: #450a0a; color: #fecaca; }

/* ── Tab bar ──────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #1a2133;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: #94a3b8 !important;
    font-weight: 500;
    font-size: 0.875rem;
    padding: 0.4rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: #1e3a5f !important;
    color: #93c5fd !important;
}
/* Tab panel background */
.stTabs [data-baseweb="tab-panel"] {
    background: transparent;
    padding-top: 1rem;
}

/* ── Buttons ──────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: #ffffff !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.875rem;
    padding: 0.55rem 1.4rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.35);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.5);
}

/* ── Inputs & textareas ───────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1e2a3e !important;
    border: 1px solid #2d3748 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    caret-color: #f1f5f9;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #4b5563 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #1e2a3e !important;
    border: 1px solid #2d3748 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
}
/* Selectbox dropdown options */
[data-baseweb="select"] * { color: #f1f5f9 !important; }
[data-baseweb="menu"] {
    background: #1e2a3e !important;
    border: 1px solid #2d3748 !important;
}
[data-baseweb="option"]:hover {
    background: #2d3f5a !important;
}

/* Input labels */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stSlider label,
.stCheckbox label, .stRadio label,
.stMultiSelect label {
    color: #cbd5e1 !important;
    font-weight: 500;
    font-size: 0.85rem;
}

/* Checkbox & radio text */
.stCheckbox span, .stRadio span {
    color: #e2e8f0 !important;
}

/* Multiselect tags */
[data-baseweb="tag"] {
    background: #1e3a5f !important;
    color: #bae6fd !important;
}

/* Slider */
[data-testid="stSlider"] .stSlider p {
    color: #cbd5e1 !important;
}

/* ── Expanders ────────────────────────────── */
/* Header (collapsed and expanded) */
[data-testid="stExpander"] > details > summary,
[data-testid="stExpander"] summary {
    background: #1e2a3e !important;
    border: 1px solid #2d3748 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 0.75rem 1rem;
}
[data-testid="stExpander"] > details[open] > summary {
    border-radius: 8px 8px 0 0 !important;
    border-bottom-color: transparent !important;
}
/* Body */
[data-testid="stExpander"] > details > div,
[data-testid="stExpander"] .streamlit-expanderContent {
    background: #1a2133 !important;
    border: 1px solid #2d3748 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    color: #e2e8f0 !important;
}
/* All text inside expander body */
[data-testid="stExpander"] details > div p,
[data-testid="stExpander"] details > div span,
[data-testid="stExpander"] details > div label,
[data-testid="stExpander"] details > div .stMarkdown {
    color: #e2e8f0 !important;
}
/* Arrow icon */
[data-testid="stExpander"] summary svg {
    fill: #94a3b8 !important;
}

/* ── Progress bar ─────────────────────────── */
.stProgress > div > div > div { background: #2563eb !important; border-radius: 999px; }
.stProgress > div > div       { background: #2d3748 !important; border-radius: 999px; }

/* ── Alerts / status boxes ────────────────── */
.stAlert > div {
    background: #1e2a3e !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── Status widget (st.status) ────────────── */
[data-testid="stStatusWidget"],
[data-testid="stStatusContainer"] {
    background: #1e2a3e !important;
    border: 1px solid #2d3748 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

/* ── Header hero ──────────────────────────── */
.hero {
    background: linear-gradient(135deg, #111827 0%, #1e2a3e 100%);
    border: 1px solid #2d3748;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
}
.hero h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 0.25rem;
}
.hero p {
    color: #94a3b8;
    font-size: 0.9rem;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: #1e3a5f;
    color: #7dd3fc;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.2em 0.7em;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* ── Divider ──────────────────────────────── */
.divider { border: none; border-top: 1px solid #2d3748; margin: 1rem 0; }

/* ── Score bar ────────────────────────────── */
.score-bar-bg {
    background: #2d3748;
    border-radius: 999px;
    height: 6px;
    width: 100%;
}
.score-bar-fill {
    background: linear-gradient(90deg, #2563eb, #60a5fa);
    border-radius: 999px;
    height: 6px;
}

/* ── Info box ─────────────────────────────── */
.info-box {
    background: #1e3a5f33;
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    color: #bae6fd;
    margin: 0.5rem 0 1rem;
}

/* ── Download button ──────────────────────── */
.stDownloadButton > button {
    background: #1e2a3e !important;
    border: 1px solid #3b82f6 !important;
    color: #93c5fd !important;
    font-weight: 500;
}

/* ── Dataframe ────────────────────────────── */
[data-testid="stDataFrame"] {
    background: #1a2133;
    border: 1px solid #2d3748;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session state initialisation
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "industry": "",
        "service": "",
        "last_url": "",
        "brand_results": [],
        "unbranded_results": [],
        "target_country": "United Kingdom",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AIAuditBot/2.0; +https://github.com/ai-audit)"
}

def get_links(url: str) -> tuple[list, str]:
    try:
        resp = requests.get(url, timeout=10, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        domain = urlparse(url).netloc
        links = {
            urljoin(url, a["href"])
            for a in soup.find_all("a", href=True)
            if urlparse(urljoin(url, a["href"])).netloc == domain
        }
        return list(links), soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return [], ""


def sentiment_badge(sentiment: str) -> str:
    cls = {"positive": "badge-positive", "negative": "badge-negative"}.get(sentiment.lower(), "badge-neutral")
    return f'<span class="badge {cls}">{sentiment}</span>'


def risk_badge(risk: str) -> str:
    cls = {"low": "badge-low", "medium": "badge-medium", "high": "badge-high"}.get(risk.lower(), "badge-neutral")
    return f'<span class="badge {cls}">{risk}</span>'


def geo_bar(score_str: str) -> str:
    try:
        score = int(score_str)
    except Exception:
        score = 5
    pct = score * 10
    colour = "#22c55e" if score >= 7 else ("#f59e0b" if score >= 4 else "#ef4444")
    return f"""
    <div style="display:flex;align-items:center;gap:8px">
        <div class="score-bar-bg" style="flex:1">
            <div class="score-bar-fill" style="width:{pct}%;background:{colour}"></div>
        </div>
        <span style="font-size:0.85rem;font-weight:600;color:{colour};min-width:24px">{score}</span>
    </div>"""


def run_audit_query(p_name, p_key, prompt, q_metadata, cat, client, comps, country, model=None, is_branded=True):
    regional_prompt = f"Context: The user is based in {country}.\n\nQuestion: {prompt}"
    result = query_llm(p_name, p_key, regional_prompt, model=model)
    answer = result.get("text", "")
    error = result.get("error")

    if error:
        analysis = {"Sentiment": "Neutral", "GEO Score": "5", "Hallucination Risk": "Low", "Entities": ""}
    else:
        analysis = analyze_response(p_name, p_key, answer, client, country, model=model)

    sov = calculate_sov(answer, client, comps)
    client_mentions = sov.get(client, 0)
    comp_mentions = {c: sov.get(c, 0) for c in comps}

    return {
        "Category": cat,
        "Funnel Stage": q_metadata.get("funnel", "N/A"),
        "Audience": q_metadata.get("audience", "General"),
        "Question": prompt,
        "Goal": q_metadata.get("goal", "N/A"),
        "Provider": p_name,
        "Model": result.get("model", model or ""),
        "Response": answer if answer else f"[Error: {error}]",
        "Error": error or "",
        "Sentiment": analysis.get("Sentiment", "Neutral"),
        "GEO Score": analysis.get("GEO Score", "5"),
        "Hallucination Risk": analysis.get("Hallucination Risk", "Low"),
        "Key Entities": analysis.get("Entities", ""),
        "Client Mentioned": "Yes" if client_mentions > 0 else "No",
        "Client Mention Count": client_mentions,
        "Competitor Mentions": ", ".join([c for c, n in comp_mentions.items() if n > 0]),
        "Competitor Mention Counts": json.dumps(comp_mentions),
    }


def results_to_csv(results: list) -> str:
    if not results:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
    return output.getvalue()


def render_results_grid(results: list, client_name: str):
    """Renders a summary chart + expandable result cards."""
    if not results:
        return

    df = pd.DataFrame(results)

    # ── Summary metrics row ────────────────────────
    total = len(df)
    mentioned = (df["Client Mentioned"] == "Yes").sum()
    sov_pct = (mentioned / total * 100) if total else 0

    sentiment_counts = df["Sentiment"].value_counts()
    pos = sentiment_counts.get("Positive", 0)
    neg = sentiment_counts.get("Negative", 0)
    neu = sentiment_counts.get("Neutral", 0)

    geo_avg = pd.to_numeric(df["GEO Score"], errors="coerce").mean()
    errors = (df["Error"] != "").sum()

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Queries", total)
    m2.metric("Brand SOV", f"{sov_pct:.1f}%", help="% of responses that mention the client brand")
    m3.metric("Avg GEO Score", f"{geo_avg:.1f}/10" if not pd.isna(geo_avg) else "N/A")
    m4.metric("Positive Sentiment", f"{pos}/{total}")
    if errors:
        m5.metric("Errors", errors, delta=f"-{errors}", delta_color="inverse")
    else:
        m5.metric("Errors", "0", delta="All OK", delta_color="normal")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Charts ─────────────────────────────────────
    chart_col1, chart_col2, chart_col3 = st.columns(3)

    with chart_col1:
        sentiment_df = df["Sentiment"].value_counts().reset_index()
        sentiment_df.columns = ["Sentiment", "Count"]
        colour_map = {"Positive": "#22c55e", "Neutral": "#60a5fa", "Negative": "#ef4444"}
        fig = px.pie(
            sentiment_df, names="Sentiment", values="Count",
            color="Sentiment", color_discrete_map=colour_map,
            hole=0.55, title="Sentiment Distribution",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_size=13, showlegend=True,
            legend=dict(font=dict(size=11, color="#94a3b8")),
            margin=dict(t=40, b=0, l=0, r=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        # Share of Voice bar
        all_names = [client_name] + [r["Competitor Mentions"].split(", ") for r in results]
        # flatten competitors
        competitors_seen = set()
        for r in results:
            for c in r["Competitor Mentions"].split(", "):
                if c:
                    competitors_seen.add(c)

        sov_data = {client_name: mentioned}
        for comp in competitors_seen:
            sov_data[comp] = sum(1 for r in results if comp in (r.get("Competitor Mentions") or ""))

        sov_df = pd.DataFrame(list(sov_data.items()), columns=["Entity", "Mentions"])
        colours = ["#2563eb"] + ["#64748b"] * (len(sov_df) - 1)
        fig2 = px.bar(
            sov_df, x="Entity", y="Mentions",
            title="Share of Voice (Mention Count)",
            color="Entity",
            color_discrete_sequence=colours,
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_size=13, showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0),
            xaxis=dict(gridcolor="#1e2535"),
            yaxis=dict(gridcolor="#1e2535"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with chart_col3:
        # GEO score by category
        df["GEO Score Num"] = pd.to_numeric(df["GEO Score"], errors="coerce")
        geo_cat = df.groupby("Category")["GEO Score Num"].mean().reset_index()
        fig3 = px.bar(
            geo_cat, x="GEO Score Num", y="Category",
            orientation="h", title="Avg GEO Score by Category",
            color="GEO Score Num",
            color_continuous_scale=["#ef4444", "#f59e0b", "#22c55e"],
            range_color=[1, 10],
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_size=13, showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=40, b=0, l=0, r=0),
            xaxis=dict(gridcolor="#1e2535", range=[0, 10]),
            yaxis=dict(gridcolor="#1e2535"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Filter controls ────────────────────────────
    fc1, fc2, fc3 = st.columns(3)
    filter_provider = fc1.multiselect(
        "Filter by Provider", options=sorted(df["Provider"].unique()), default=list(df["Provider"].unique()), key=f"fp_{id(results)}"
    )
    filter_sentiment = fc2.multiselect(
        "Filter by Sentiment", options=["Positive", "Neutral", "Negative"], default=["Positive", "Neutral", "Negative"], key=f"fs_{id(results)}"
    )
    filter_mentioned = fc3.radio(
        "Client Mentioned", ["All", "Yes", "No"], horizontal=True, key=f"fm_{id(results)}"
    )

    filtered = df[
        df["Provider"].isin(filter_provider) &
        df["Sentiment"].isin(filter_sentiment)
    ]
    if filter_mentioned != "All":
        filtered = filtered[filtered["Client Mentioned"] == filter_mentioned]

    st.caption(f"Showing {len(filtered)} of {total} results")

    # ── Result cards ───────────────────────────────
    for _, row in filtered.iterrows():
        icon = "✅" if row["Client Mentioned"] == "Yes" else "⬜"
        label = f"{icon} {row['Question'][:90]}{'...' if len(row['Question']) > 90 else ''} — *{row['Provider']}* ({row['Model']})"
        with st.expander(label):
            col_a, col_b, col_c = st.columns([1, 1, 2])

            with col_a:
                st.markdown(f"**Sentiment**<br>{sentiment_badge(row['Sentiment'])}", unsafe_allow_html=True)
                st.markdown(f"**Hallucination Risk**<br>{risk_badge(row['Hallucination Risk'])}", unsafe_allow_html=True)

            with col_b:
                st.markdown(f"**GEO Score**")
                st.markdown(geo_bar(row["GEO Score"]), unsafe_allow_html=True)
                st.markdown(f"**Funnel Stage**<br><span style='color:#94a3b8;font-size:0.8rem'>{row['Funnel Stage']}</span>", unsafe_allow_html=True)

            with col_c:
                st.markdown(f"**Goal:** *{row['Goal']}*")
                if row.get("Key Entities"):
                    st.markdown(f"**Entities:** {row['Key Entities']}")
                if row["Client Mentioned"] == "Yes":
                    st.success(f"Brand mentioned {row['Client Mention Count']}x in this response")
                if row["Competitor Mentions"]:
                    st.warning(f"Competitors mentioned: {row['Competitor Mentions']}")
                if row.get("Error"):
                    st.error(f"API Error: {row['Error']}")

            st.markdown("**Full Response:**")
            st.markdown(f"<div style='background:#0f1117;border-radius:8px;padding:1rem;font-size:0.85rem;color:#cbd5e1;line-height:1.6;white-space:pre-wrap'>{row['Response']}</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙ Global Settings")

    with st.expander("🔑 API Keys", expanded=True):
        openai_key = st.text_input("OpenAI API Key", type="password", key="oai_key",
            help="Required for OpenAI models. Never stored.")
        openai_model = st.selectbox("OpenAI Model", OPENAI_MODELS, index=0, key="oai_model")

        st.divider()

        gemini_key = st.text_input("Gemini API Key", type="password", key="gem_key",
            help="Required for Google Gemini models. Never stored.")
        gemini_model = st.selectbox("Gemini Model", GEMINI_MODELS, index=1, key="gem_model")

    with st.expander("🌍 Region & Context", expanded=True):
        country = st.selectbox(
            "Target Country/Region",
            ["United Kingdom", "United States", "Canada", "Australia", "Germany", "France", "Ireland", "Other"],
            index=0,
        )
        st.session_state["target_country"] = country

    with st.expander("⚡ Performance", expanded=False):
        max_workers = st.slider("Parallel Workers", 1, 20, 8, help="Higher = faster but more likely to hit API rate limits.")
        skip_analysis = st.checkbox(
            "Skip per-response analysis",
            value=False,
            help="Skips the secondary LLM analysis call for each response. Results run faster but without Sentiment/GEO/Hallucination scores.",
        )

    st.divider()
    if st.session_state.get("brand_results") or st.session_state.get("unbranded_results"):
        st.markdown("### 📦 Export All Results")
        all_results = st.session_state.get("brand_results", []) + st.session_state.get("unbranded_results", [])
        st.download_button(
            "⬇ Download Combined CSV",
            results_to_csv(all_results),
            "ai_audit_combined.csv",
            "text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    st.caption("AI Visibility Audit Suite v2.0")


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">GEO Audit Tool</div>
    <h1>AI Visibility &amp; Discovery Audit Suite</h1>
    <p>Measure how AI models perceive, rank, and recommend your brand — and where competitors have the edge.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SHARED INPUTS
# ─────────────────────────────────────────────
with st.container():
    st.markdown("### 🏢 Client & Context Setup")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        client_name = st.text_input("Client / Brand Name", placeholder="e.g. Acme Corp",
            help="Injected into {client} placeholders across all prompts.")
        website_url = st.text_input("Website URL", placeholder="https://www.acme.com",
            help="Used to auto-detect industry, services, and discovery keywords.")

    with col2:
        detect_col, _ = st.columns([3, 1])
        with detect_col:
            detect_btn = st.button("🔍 Auto-detect Industry", use_container_width=True,
                help="Crawls the website and uses an LLM to detect industry and core service.")

        if detect_btn and website_url and (openai_key or gemini_key):
            with st.spinner("Crawling website and detecting industry..."):
                _, text = get_links(website_url)
                p_name = "OpenAI" if openai_key else "Gemini"
                p_key = openai_key if openai_key else gemini_key
                p_model = openai_model if openai_key else gemini_model
                prompt = f"Based on this website text, identify the specific industry and the primary core service/product offered. Return ONLY in this format: Industry | Service\n\n{text[:2500]}"
                res = query_llm(p_name, p_key, prompt, model=p_model)
                if "|" in res.get("text", ""):
                    ind, svc = [x.strip() for x in res["text"].split("|", 1)]
                    st.session_state["industry"] = ind
                    st.session_state["service"] = svc
                    st.session_state["last_url"] = website_url
                    st.success(f"Detected: **{ind}** — *{svc}*")
                elif res.get("error"):
                    st.error(f"Detection failed: {res['error']}")
                else:
                    st.warning("Could not parse response — please enter manually.")

        industry = st.text_input("Industry", value=st.session_state.get("industry", ""),
            placeholder="e.g. financial services", help="Injected into {industry} placeholders.")
        core_service = st.text_input("Core Service", value=st.session_state.get("service", ""),
            placeholder="e.g. wealth management", help="Injected into {service} placeholders.")

    with col3:
        competitor_input = st.text_area("Competitors (1 per line, max 5)",
            placeholder="Competitor A\nCompetitor B\nCompetitor C",
            height=140, help="Used for Share of Voice tracking and direct comparisons.")
        competitors = [c.strip() for c in competitor_input.split("\n") if c.strip()][:5]


st.divider()


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏷 Brand Audit", "🌐 Unbranded Audit", "📊 Combined Dashboard"])


# ─────────────────────────────────────────────
# TAB 1 — BRAND AUDIT
# ─────────────────────────────────────────────
with tab1:
    st.markdown("#### Brand Perception Audit")
    st.markdown(
        "<div class='info-box'>Query LLMs with questions that <strong>specifically mention your brand</strong>. "
        "Results reveal how AI models perceive, position, and discuss your brand vs competitors.</div>",
        unsafe_allow_html=True,
    )

    cat_help = {
        "Core Brand Signals": "Checks if the LLM knows basic facts, slogans, and regulatory status of your brand.",
        "Market Comparisons": "Directly compares your brand against the listed competitors.",
        "Customer Persona Highlights": "Tests how your brand is pitched to specific audience segments.",
        "Reputation Under Pressure": "Forces the LLM to identify disadvantages, risks, and complaints about your brand.",
    }

    bcol1, bcol2 = st.columns(2)
    selected_cats = []
    cat_list = list(BRANDED_CATEGORIES.keys())
    for i, cat in enumerate(cat_list):
        col = bcol1 if i % 2 == 0 else bcol2
        count = len(BRANDED_CATEGORIES[cat])
        checked = col.checkbox(f"{cat} ({count} questions)", key=f"branded_cat_{cat}", help=cat_help.get(cat, ""))
        if checked:
            selected_cats.append(cat)

    custom_questions_input = st.text_area(
        "Custom Branded Questions (1 per line)",
        placeholder="How does {client} handle {industry} regulations?\nIs {client} better than {competitors}?",
        help="Use {client}, {industry}, {service}, {competitors} as dynamic placeholders.",
        height=90,
    )
    custom_questions = [q.strip() for q in custom_questions_input.split("\n") if q.strip()]

    run_brand = st.button("▶ Run Brand Audit", type="primary", use_container_width=False)

    if run_brand:
        if not (openai_key or gemini_key):
            st.error("Please provide at least one API key in the sidebar.")
        elif not client_name:
            st.error("Please provide a Client Name above.")
        elif not selected_cats and not custom_questions:
            st.warning("Select at least one category or add a custom question.")
        else:
            providers = []
            if openai_key:
                providers.append(("OpenAI", openai_key, openai_model))
            if gemini_key:
                providers.append(("Gemini", gemini_key, gemini_model))

            all_tasks = []
            for cat in selected_cats:
                for q_data in BRANDED_CATEGORIES[cat]:
                    display_q = format_prompt(q_data["question"], client_name, competitors, country, industry, core_service)
                    for p_name, p_key, p_model in providers:
                        all_tasks.append((p_name, p_key, display_q, q_data, cat, client_name, competitors, country, p_model))

            for cq in custom_questions:
                display_q = cq.replace("{client}", client_name).replace("{competitors}", ", ".join(competitors)).replace("{industry}", industry).replace("{service}", core_service)
                for p_name, p_key, p_model in providers:
                    all_tasks.append((p_name, p_key, display_q, {}, "Custom", client_name, competitors, country, p_model))

            st.info(f"Running {len(all_tasks)} branded queries across {len(providers)} provider(s)...")
            progress_bar = st.progress(0)
            status_text = st.empty()

            brand_results = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(run_audit_query, t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8]): i
                    for i, t in enumerate(all_tasks)
                }
                completed = 0
                for future in as_completed(futures):
                    try:
                        brand_results.append(future.result())
                    except Exception as e:
                        brand_results.append({"Error": str(e), "Question": "Unknown", "Provider": "Unknown"})
                    completed += 1
                    progress_bar.progress(completed / len(all_tasks))
                    status_text.caption(f"Completed {completed} / {len(all_tasks)} queries")

            status_text.empty()
            st.session_state["brand_results"] = brand_results
            st.success(f"Brand audit complete — {len(brand_results)} results.")

    if st.session_state.get("brand_results"):
        st.divider()
        st.markdown("### Brand Audit Results")
        render_results_grid(st.session_state["brand_results"], client_name or "Your Brand")
        st.download_button(
            "⬇ Download Brand Audit CSV",
            results_to_csv(st.session_state["brand_results"]),
            "brand_audit.csv",
            "text/csv",
        )


# ─────────────────────────────────────────────
# TAB 2 — UNBRANDED AUDIT
# ─────────────────────────────────────────────
with tab2:
    st.markdown("#### Unbranded Visibility Audit")
    st.markdown(
        "<div class='info-box'>Ask the LLMs generic industry questions <strong>without mentioning your brand</strong>. "
        "If your brand appears in the response, that counts as earned AI share of voice.</div>",
        unsafe_allow_html=True,
    )

    uc1, uc2 = st.columns(2)
    selected_unbranded_cats = []
    ucat_list = list(UNBRANDED_CATEGORIES.keys())
    for i, cat in enumerate(ucat_list):
        col = uc1 if i % 2 == 0 else uc2
        count = len(UNBRANDED_CATEGORIES[cat])
        checked = col.checkbox(f"{cat} ({count} questions)", value=True, key=f"unbranded_cat_{cat}")
        if checked:
            selected_unbranded_cats.append(cat)

    st.markdown("##### Keyword Discovery")
    kw_col1, kw_col2 = st.columns(2)
    with kw_col1:
        manual_keywords = st.text_area(
            "Manual Keywords (Optional, 1 per line)",
            placeholder="wealth management\nfinancial planning\nISA advice",
            help="Leave blank to auto-generate from your website.",
            height=100,
        )
    with kw_col2:
        use_auto_keywords = st.checkbox("Auto-generate keywords from website", value=True,
            help="Crawls your website and uses an LLM to extract unbranded discovery keywords.")
        kw_count = st.slider("Keywords to generate", 3, 10, 5, help="Only applies to auto-generation.")

    run_unbranded = st.button("▶ Run Unbranded Audit", type="primary")

    if run_unbranded:
        if not (openai_key or gemini_key):
            st.error("Please provide at least one API key in the sidebar.")
        elif not client_name:
            st.error("Please provide a Client Name above.")
        else:
            providers = []
            if openai_key:
                providers.append(("OpenAI", openai_key, openai_model))
            if gemini_key:
                providers.append(("Gemini", gemini_key, gemini_model))

            p_name_kw, p_key_kw, p_model_kw = providers[0]

            with st.status("Running Unbranded Audit...", expanded=True) as status:
                all_unbranded_tasks = []

                # Category questions
                for cat in selected_unbranded_cats:
                    for q_data in UNBRANDED_CATEGORIES[cat]:
                        display_q = format_prompt(q_data["question"], client_name, competitors, country, industry, core_service)
                        for pn, pk, pm in providers:
                            all_unbranded_tasks.append((pn, pk, display_q, q_data, cat, client_name, competitors, country, pm))

                # Keyword discovery
                if use_auto_keywords or manual_keywords:
                    st.write("Gathering keywords...")

                    if manual_keywords.strip():
                        keywords = [k.strip() for k in manual_keywords.split("\n") if k.strip()]
                    else:
                        keywords = []

                    if use_auto_keywords and website_url:
                        links, home_text = get_links(website_url)
                        combined_text = home_text
                        for link in links[:3]:
                            _, sub_text = get_links(link)
                            combined_text += " " + sub_text

                        kw_prompt = (
                            f"Context: {country}, Industry: {industry}. "
                            f"Identify {kw_count} unbranded SEO keywords a potential customer would search when looking for {core_service or 'services in this industry'}. "
                            f"Return ONLY keywords, one per line:\n\n{combined_text[:4000]}"
                        )
                        kw_result = query_llm(p_name_kw, p_key_kw, kw_prompt, model=p_model_kw)
                        if not kw_result.get("error"):
                            auto_kws = [k.strip() for k in kw_result["text"].split("\n") if k.strip()][:kw_count]
                            keywords = list(dict.fromkeys(keywords + auto_kws))  # deduplicate, preserve order

                    if keywords:
                        st.write(f"Keywords: **{', '.join(keywords)}**")

                        for kw in keywords:
                            q_prompt = (
                                f"Context: {country}, Industry: {industry}. "
                                f"Generate 3 unbranded informational questions a user might ask about '{kw}'. "
                                f"Return ONLY questions, one per line."
                            )
                            q_result = query_llm(p_name_kw, p_key_kw, q_prompt, model=p_model_kw)
                            if not q_result.get("error"):
                                kw_qs = [q.strip() for q in q_result["text"].split("\n") if q.strip()][:3]
                                for q in kw_qs:
                                    for pn, pk, pm in providers:
                                        all_unbranded_tasks.append((
                                            pn, pk, q,
                                            {"funnel": "Discovery", "goal": f"Keyword discovery: {kw}", "audience": "General"},
                                            "Keyword Discovery",
                                            client_name, competitors, country, pm
                                        ))

                status.update(label=f"Querying LLMs ({len(all_unbranded_tasks)} questions)...", state="running")
                progress_bar_u = st.progress(0)
                unbranded_results = []

                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {
                        executor.submit(run_audit_query, t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8]): i
                        for i, t in enumerate(all_unbranded_tasks)
                    }
                    completed = 0
                    for future in as_completed(futures):
                        try:
                            unbranded_results.append(future.result())
                        except Exception as e:
                            pass
                        completed += 1
                        progress_bar_u.progress(completed / len(all_unbranded_tasks))

                st.session_state["unbranded_results"] = unbranded_results
                status.update(label=f"Complete — {len(unbranded_results)} results.", state="complete")

    if st.session_state.get("unbranded_results"):
        st.divider()
        st.markdown("### Unbranded Audit Results")
        render_results_grid(st.session_state["unbranded_results"], client_name or "Your Brand")
        st.download_button(
            "⬇ Download Unbranded Audit CSV",
            results_to_csv(st.session_state["unbranded_results"]),
            "unbranded_audit.csv",
            "text/csv",
        )


# ─────────────────────────────────────────────
# TAB 3 — COMBINED DASHBOARD
# ─────────────────────────────────────────────
with tab3:
    brand_res = st.session_state.get("brand_results", [])
    unbranded_res = st.session_state.get("unbranded_results", [])
    all_res = brand_res + unbranded_res

    if not all_res:
        st.info("Run a Brand Audit and/or Unbranded Audit to see combined results here.")
    else:
        st.markdown("### Combined Audit Dashboard")
        df_all = pd.DataFrame(all_res)

        total = len(df_all)
        mentioned = (df_all["Client Mentioned"] == "Yes").sum()
        geo_avg = pd.to_numeric(df_all["GEO Score"], errors="coerce").mean()
        error_count = (df_all.get("Error", pd.Series([""] * total)) != "").sum()

        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Total Queries", total, help="Combined branded + unbranded")
        d2.metric("Overall Brand SOV", f"{mentioned/total*100:.1f}%" if total else "N/A")
        d3.metric("Avg GEO Score", f"{geo_avg:.1f}/10" if not pd.isna(geo_avg) else "N/A")
        d4.metric("Failed Queries", int(error_count))

        st.divider()

        dcol1, dcol2 = st.columns(2)

        with dcol1:
            # SOV by audit type
            b_mentioned = sum(1 for r in brand_res if r.get("Client Mentioned") == "Yes") if brand_res else 0
            u_mentioned = sum(1 for r in unbranded_res if r.get("Client Mentioned") == "Yes") if unbranded_res else 0
            sov_compare = pd.DataFrame({
                "Audit Type": ["Brand Audit", "Unbranded Audit"],
                "SOV %": [
                    (b_mentioned / len(brand_res) * 100) if brand_res else 0,
                    (u_mentioned / len(unbranded_res) * 100) if unbranded_res else 0,
                ],
            })
            fig_sov = px.bar(
                sov_compare, x="Audit Type", y="SOV %",
                title="Brand SOV by Audit Type",
                color="Audit Type",
                color_discrete_sequence=["#2563eb", "#06b6d4"],
            )
            fig_sov.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", title_font_size=13, showlegend=False,
                margin=dict(t=40, b=0, l=0, r=0),
                yaxis=dict(gridcolor="#1e2535", range=[0, 100]),
                xaxis=dict(gridcolor="#1e2535"),
            )
            st.plotly_chart(fig_sov, use_container_width=True)

        with dcol2:
            # Sentiment breakdown by provider
            if "Provider" in df_all.columns:
                sent_prov = df_all.groupby(["Provider", "Sentiment"]).size().reset_index(name="Count")
                fig_sp = px.bar(
                    sent_prov, x="Provider", y="Count", color="Sentiment",
                    title="Sentiment by Provider",
                    color_discrete_map={"Positive": "#22c55e", "Neutral": "#60a5fa", "Negative": "#ef4444"},
                    barmode="stack",
                )
                fig_sp.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0", title_font_size=13,
                    margin=dict(t=40, b=0, l=0, r=0),
                    yaxis=dict(gridcolor="#1e2535"),
                    xaxis=dict(gridcolor="#1e2535"),
                    legend=dict(font=dict(color="#94a3b8")),
                )
                st.plotly_chart(fig_sp, use_container_width=True)

        st.divider()

        # Full data table
        st.markdown("#### Full Results Table")
        display_cols = ["Category", "Funnel Stage", "Provider", "Model", "Sentiment", "GEO Score", "Hallucination Risk", "Client Mentioned", "Competitor Mentions", "Question"]
        available_cols = [c for c in display_cols if c in df_all.columns]
        st.dataframe(
            df_all[available_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "GEO Score": st.column_config.NumberColumn(format="%d/10"),
                "Question": st.column_config.TextColumn(width="large"),
            }
        )

        st.download_button(
            "⬇ Download Full Combined CSV",
            results_to_csv(all_res),
            "ai_audit_full.csv",
            "text/csv",
        )

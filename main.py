import streamlit as st
import csv
import io
import json
import time
import requests
import pandas as pd
import plotly.express as px
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.llm_handler import query_llm, OPENAI_MODELS, GEMINI_MODELS, PERPLEXITY_MODELS
from utils.prompts import BRANDED_CATEGORIES, UNBRANDED_CATEGORIES, format_prompt
from utils.analysis import analyze_response, calculate_sov, calculate_geo_score
from utils.profiles import (
    list_profiles, save_profile, load_profile, delete_profile, profile_to_dict,
)
from utils.cache import get_cached, set_cached, cache_stats, clear_cache
from utils.recommendations import generate_recommendation, should_flag_for_recommendation

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Visibility Audit",
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
.stCheckbox span, .stRadio span {
    color: #e2e8f0 !important;
}
[data-baseweb="tag"] {
    background: #1e3a5f !important;
    color: #bae6fd !important;
}
[data-testid="stSlider"] .stSlider p {
    color: #cbd5e1 !important;
}

/* ── Expanders ────────────────────────────── */
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
[data-testid="stExpander"] > details > div,
[data-testid="stExpander"] .streamlit-expanderContent {
    background: #1a2133 !important;
    border: 1px solid #2d3748 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    color: #e2e8f0 !important;
}
[data-testid="stExpander"] details > div p,
[data-testid="stExpander"] details > div span,
[data-testid="stExpander"] details > div label,
[data-testid="stExpander"] details > div .stMarkdown {
    color: #e2e8f0 !important;
}
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
[data-testid="stStatusWidget"],
[data-testid="stStatusContainer"] {
    background: #1e2a3e !important;
    border: 1px solid #2d3748 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

/* ── Hero ─────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #111827 0%, #1e2a3e 100%);
    border: 1px solid #2d3748;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
}
.hero h1 { font-size: 1.75rem; font-weight: 700; color: #f8fafc; margin: 0 0 0.25rem; }
.hero p  { color: #94a3b8; font-size: 0.9rem; margin: 0; }
.hero-badge {
    display: inline-block;
    background: #1e3a5f; color: #7dd3fc;
    border-radius: 999px; font-size: 0.7rem; font-weight: 600;
    padding: 0.2em 0.7em; letter-spacing: 0.05em;
    text-transform: uppercase; margin-bottom: 0.6rem;
}

/* ── Misc ─────────────────────────────────── */
.divider { border: none; border-top: 1px solid #2d3748; margin: 1rem 0; }
.score-bar-bg  { background: #2d3748; border-radius: 999px; height: 6px; width: 100%; }
.score-bar-fill { background: linear-gradient(90deg, #2563eb, #60a5fa); border-radius: 999px; height: 6px; }
.info-box {
    background: #1e3a5f33; border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0; padding: 0.75rem 1rem;
    font-size: 0.85rem; color: #bae6fd; margin: 0.5rem 0 1rem;
}
.stDownloadButton > button {
    background: #1e2a3e !important; border: 1px solid #3b82f6 !important;
    color: #93c5fd !important; font-weight: 500;
}
[data-testid="stDataFrame"] {
    background: #1a2133; border: 1px solid #2d3748; border-radius: 8px;
}
/* Fix-it brief box */
.fixbox {
    background: #1a2e1a; border: 1px solid #166534; border-radius: 8px;
    padding: 1rem 1.25rem; font-size: 0.85rem; color: #d1fae5; line-height: 1.7;
    white-space: pre-wrap; margin-top: 0.75rem;
}
/* Citation pill */
.cite-pill {
    display: inline-block; background: #1e3a5f; color: #93c5fd;
    border-radius: 4px; font-size: 0.7rem; padding: 0.15em 0.5em;
    margin: 0.1em; word-break: break-all;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "industry": "", "service": "", "last_url": "",
        "brand_results": [], "unbranded_results": [],
        "target_country": "United Kingdom",
        "custom_branded_q": {},    # Feature 9: {cat: [extra questions]}
        "custom_unbranded_q": {},  # Feature 9
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AIAuditBot/2.0)"}


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
    except Exception:
        return [], ""


def sentiment_badge(s: str) -> str:
    cls = {"positive": "badge-positive", "negative": "badge-negative"}.get(s.lower(), "badge-neutral")
    return f'<span class="badge {cls}">{s}</span>'


def risk_badge(r: str) -> str:
    cls = {"low": "badge-low", "medium": "badge-medium", "high": "badge-high"}.get(r.lower(), "badge-neutral")
    return f'<span class="badge {cls}">{r}</span>'


def geo_bar(score_str: str) -> str:
    try:
        score = int(score_str)
    except Exception:
        score = 5
    pct = score * 10
    colour = "#22c55e" if score >= 7 else ("#f59e0b" if score >= 4 else "#ef4444")
    return (
        f'<div style="display:flex;align-items:center;gap:8px">'
        f'<div class="score-bar-bg" style="flex:1">'
        f'<div class="score-bar-fill" style="width:{pct}%;background:{colour}"></div></div>'
        f'<span style="font-size:0.85rem;font-weight:600;color:{colour};min-width:24px">{score}</span></div>'
    )


def run_audit_query(p_name, p_key, prompt, q_metadata, cat, client, comps, country, model=None, use_cache=True):
    """Run a single query — uses cache if available (Feature 2)."""
    regional_prompt = f"Context: The user is based in {country}.\n\nQuestion: {prompt}"

    # ── Feature 2: check cache ────────────────
    cached = get_cached(p_name, model or "", regional_prompt) if use_cache else None
    if cached:
        return {**cached, "_from_cache": True}

    result = query_llm(p_name, p_key, regional_prompt, model=model)
    answer = result.get("text", "")
    error = result.get("error")
    citations = result.get("citations", [])  # Feature 12

    if error:
        analysis = {"Sentiment": "Neutral", "Hallucination Risk": "Low", "Entities": ""}
        sov = {client: 0}
        for c in comps: sov[c] = 0
    else:
        analysis = analyze_response(p_name, p_key, answer, client, country, model=model)
        sov = calculate_sov(answer, client, comps)

    # Deterministic GEO Score calculation
    geo_score = calculate_geo_score(answer, client, analysis.get("Sentiment", "Neutral"), sov)

    client_mentions = sov.get(client, 0)
    comp_mentions = {c: sov.get(c, 0) for c in comps}

    row = {
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
        "GEO Score": geo_score,
        "Hallucination Risk": analysis.get("Hallucination Risk", "Low"),
        "Key Entities": analysis.get("Entities", ""),
        "Client Mentioned": "Yes" if client_mentions > 0 else "No",
        "Client Mention Count": client_mentions,
        "Competitor Mentions": ", ".join([c for c, n in comp_mentions.items() if n > 0]),
        "Competitor Mention Counts": json.dumps(comp_mentions),
        "Citations": json.dumps(citations),   # Feature 12
        "_from_cache": False,
    }

    # ── Feature 2: store in cache ─────────────
    if use_cache and not error:
        set_cached(p_name, model or "", regional_prompt, row)

    return row


def results_to_csv(results: list) -> str:
    if not results:
        return ""
    # Exclude internal keys from export
    skip = {"_from_cache"}
    keys = [k for k in results[0].keys() if k not in skip]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=keys, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(results)
    return output.getvalue()


def render_citations(citations_json: str):
    """Feature 12: render citation pills from a JSON list of URLs."""
    try:
        urls = json.loads(citations_json) if citations_json else []
    except Exception:
        urls = []
    if not urls:
        return
    st.markdown("**Citations found in response:**")
    pills = " ".join(
        f'<a href="{u}" target="_blank" class="cite-pill">{u[:60]}{"…" if len(u) > 60 else ""}</a>'
        for u in urls[:10]
    )
    st.markdown(pills, unsafe_allow_html=True)


def render_results_grid(results: list, client_name: str, provider_for_recs: tuple | None = None):
    """Renders summary metrics, charts, filters, and result cards."""
    if not results:
        return

    df = pd.DataFrame(results)

    total = len(df)
    mentioned = (df["Client Mentioned"] == "Yes").sum()
    sov_pct = (mentioned / total * 100) if total else 0
    geo_avg = pd.to_numeric(df["GEO Score"], errors="coerce").mean()
    errors = (df["Error"] != "").sum()
    cached_count = df.get("_from_cache", pd.Series([False] * total)).sum()
    pos = (df["Sentiment"] == "Positive").sum()

    # ── Metrics ───────────────────────────────
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Queries", total)
    m2.metric("Brand SOV", f"{sov_pct:.1f}%")
    m3.metric("Avg GEO Score", f"{geo_avg:.1f}/10" if not pd.isna(geo_avg) else "N/A")
    m4.metric("Positive Sentiment", f"{pos}/{total}")
    m5.metric("From Cache", int(cached_count), help="Queries served from local cache (Feature 2)")
    if errors:
        m6.metric("Errors", int(errors), delta=f"-{int(errors)}", delta_color="inverse")
    else:
        m6.metric("Errors", "0", delta="All OK", delta_color="normal")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────
    chart_col1, chart_col2, chart_col3 = st.columns(3)

    with chart_col1:
        sent_df = df["Sentiment"].value_counts().reset_index()
        sent_df.columns = ["Sentiment", "Count"]
        fig = px.pie(
            sent_df, names="Sentiment", values="Count",
            color="Sentiment",
            color_discrete_map={"Positive": "#22c55e", "Neutral": "#60a5fa", "Negative": "#ef4444"},
            hole=0.55, title="Sentiment Distribution",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_size=13,
            legend=dict(font=dict(size=11, color="#94a3b8")),
            margin=dict(t=40, b=0, l=0, r=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        competitors_seen = set()
        for r in results:
            for c in (r.get("Competitor Mentions") or "").split(", "):
                if c:
                    competitors_seen.add(c)
        sov_data = {client_name: int(mentioned)}
        for comp in competitors_seen:
            sov_data[comp] = sum(1 for r in results if comp in (r.get("Competitor Mentions") or ""))
        sov_df = pd.DataFrame(list(sov_data.items()), columns=["Entity", "Mentions"])
        colours = ["#2563eb"] + ["#64748b"] * (len(sov_df) - 1)
        fig2 = px.bar(sov_df, x="Entity", y="Mentions", title="Share of Voice",
                      color="Entity", color_discrete_sequence=colours)
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_size=13, showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0),
            xaxis=dict(gridcolor="#2d3748"), yaxis=dict(gridcolor="#2d3748"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with chart_col3:
        df["GEO Score Num"] = pd.to_numeric(df["GEO Score"], errors="coerce")
        geo_cat = df.groupby("Category")["GEO Score Num"].mean().reset_index()
        fig3 = px.bar(
            geo_cat, x="GEO Score Num", y="Category", orientation="h",
            title="Avg GEO Score by Category",
            color="GEO Score Num",
            color_continuous_scale=["#ef4444", "#f59e0b", "#22c55e"],
            range_color=[1, 10],
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0", title_font_size=13, showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=40, b=0, l=0, r=0),
            xaxis=dict(gridcolor="#2d3748", range=[0, 10]),
            yaxis=dict(gridcolor="#2d3748"),
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Filters ───────────────────────────────
    fc1, fc2, fc3, fc4 = st.columns(4)
    filter_provider = fc1.multiselect(
        "Provider", options=sorted(df["Provider"].unique()),
        default=list(df["Provider"].unique()), key=f"fp_{id(results)}"
    )
    filter_sentiment = fc2.multiselect(
        "Sentiment", options=["Positive", "Neutral", "Negative"],
        default=["Positive", "Neutral", "Negative"], key=f"fs_{id(results)}"
    )
    filter_mentioned = fc3.radio(
        "Client Mentioned", ["All", "Yes", "No"], horizontal=True, key=f"fm_{id(results)}"
    )
    filter_flagged = fc4.checkbox(
        "Show fix-it candidates only", key=f"ff_{id(results)}",
        help="Only show results with low GEO score, negative sentiment, or high hallucination risk."
    )

    filtered = df[df["Provider"].isin(filter_provider) & df["Sentiment"].isin(filter_sentiment)]
    if filter_mentioned != "All":
        filtered = filtered[filtered["Client Mentioned"] == filter_mentioned]
    if filter_flagged:
        filtered = filtered[filtered.apply(lambda r: should_flag_for_recommendation(r.to_dict()), axis=1)]

    st.caption(f"Showing {len(filtered)} of {total} results")

    # ── Result cards ──────────────────────────
    for _, row in filtered.iterrows():
        icon = "✅" if row["Client Mentioned"] == "Yes" else "⬜"
        flag = "⚠️ " if should_flag_for_recommendation(row.to_dict()) else ""
        cache_tag = " 💾" if row.get("_from_cache") else ""
        label = f"{flag}{icon} {row['Question'][:85]}{'…' if len(row['Question']) > 85 else ''} — {row['Provider']} ({row['Model']}){cache_tag}"

        with st.expander(label):
            col_a, col_b, col_c = st.columns([1, 1, 2])

            with col_a:
                st.markdown(f"**Sentiment**<br>{sentiment_badge(row['Sentiment'])}", unsafe_allow_html=True)
                st.markdown(f"**Hallucination Risk**<br>{risk_badge(row['Hallucination Risk'])}", unsafe_allow_html=True)

            with col_b:
                st.markdown("**GEO Score**")
                st.markdown(geo_bar(row["GEO Score"]), unsafe_allow_html=True)
                st.markdown(
                    f"**Funnel**<br><span style='color:#94a3b8;font-size:0.8rem'>{row['Funnel Stage']}</span>",
                    unsafe_allow_html=True,
                )

            with col_c:
                st.markdown(f"**Goal:** *{row['Goal']}*")
                if row.get("Key Entities"):
                    st.markdown(f"**Entities:** {row['Key Entities']}")
                if row["Client Mentioned"] == "Yes":
                    st.success(f"Brand mentioned {row['Client Mention Count']}× in this response")
                if row["Competitor Mentions"]:
                    st.warning(f"Competitors mentioned: {row['Competitor Mentions']}")
                if row.get("Error"):
                    st.error(f"API Error: {row['Error']}")

            # Feature 12: citations
            render_citations(row.get("Citations", "[]"))

            st.markdown("**Full Response:**")
            st.markdown(
                f"<div style='background:#0d1117;border-radius:8px;padding:1rem;"
                f"font-size:0.85rem;color:#cbd5e1;line-height:1.6;white-space:pre-wrap'>"
                f"{row['Response']}</div>",
                unsafe_allow_html=True,
            )

            # Feature 8: fix-it recommendation
            if should_flag_for_recommendation(row.to_dict()) and provider_for_recs:
                p_name_r, p_key_r, p_model_r, industry_r, country_r = provider_for_recs
                if st.button("💡 Generate Fix-it Brief", key=f"fix_{hash(row['Question'] + row['Provider'])}"):
                    with st.spinner("Generating content recommendation…"):
                        rec = generate_recommendation(
                            row.to_dict(), client_name, industry_r, country_r,
                            p_name_r, p_key_r, p_model_r,
                        )
                    st.markdown(f"<div class='fixbox'>{rec}</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙ Global Settings")

    # ── Feature 1: Profiles ───────────────────
    with st.expander("Client Profiles", expanded=False):
        profiles = list_profiles()
        if profiles:
            load_name = st.selectbox("Load profile", ["— select —"] + profiles, key="load_profile_sel")
            lcol, dcol = st.columns(2)
            if lcol.button("Load", use_container_width=True, key="load_profile_btn"):
                p = load_profile(load_name)
                if p:
                    for k in ["client_name", "website_url", "industry", "core_service", "country"]:
                        if k in p:
                            st.session_state[k if k not in ("industry", "core_service") else k] = p[k]
                    st.session_state["industry"] = p.get("industry", "")
                    st.session_state["service"] = p.get("core_service", "")
                    st.session_state["_loaded_profile"] = p
                    st.success(f"Loaded '{load_name}'")
            if dcol.button("Delete", use_container_width=True, key="del_profile_btn"):
                delete_profile(load_name)
                st.success(f"Deleted '{load_name}'")
                st.rerun()
        else:
            st.caption("No saved profiles yet.")

        save_name = st.text_input("Save current setup as…", placeholder="Client name", key="save_profile_name")
        if st.button("Save Profile", use_container_width=True, key="save_profile_btn"):
            if save_name:
                st.session_state["_pending_save"] = save_name
            else:
                st.warning("Enter a name first.")

    # ── API Keys ──────────────────────────────
    with st.expander("API Keys", expanded=True):
        openai_key = st.text_input("OpenAI API Key", type="password", key="oai_key",
            help="Required for OpenAI models. Never stored.")
        openai_model = st.selectbox("OpenAI Model", OPENAI_MODELS, index=0, key="oai_model")
        st.divider()
        gemini_key = st.text_input("Gemini API Key", type="password", key="gem_key",
            help="Required for Google Gemini models. Never stored.")
        gemini_model = st.selectbox("Gemini Model", GEMINI_MODELS, index=0, key="gem_model")
        st.divider()
        # Feature 6: Perplexity
        perplexity_key = st.text_input("Perplexity API Key", type="password", key="pplx_key",
            help="Required for Perplexity Sonar models. Uses live web search — great for citation tracking.")
        perplexity_model = st.selectbox("Perplexity Model", PERPLEXITY_MODELS, index=0, key="pplx_model")

    with st.expander("Region & Context", expanded=True):
        country = st.selectbox(
            "Target Country/Region",
            ["United Kingdom", "United States", "Canada", "Australia", "Germany", "France", "Ireland", "Other"],
            index=0, key="country_sel",
        )
        st.session_state["target_country"] = country

    with st.expander("⚡ Performance", expanded=False):
        max_workers = st.slider("Parallel Workers", 1, 20, 8,
            help="Higher = faster but more likely to hit API rate limits.")
        use_cache = st.checkbox("Use result cache", value=True,
            help="Skip API calls for queries already run before (Feature 2).")
        skip_analysis = st.checkbox("Skip per-response analysis", value=False,
            help="Faster but skips Sentiment/GEO/Hallucination scoring.")

    # ── Feature 2: Cache stats + clear ────────
    with st.expander("Cache", expanded=False):
        stats = cache_stats()
        st.metric("Cached entries", stats["entries"])
        st.metric("Cache size", f"{stats['size_kb']} KB")
        if st.button("Clear Cache", use_container_width=True, key="clear_cache_btn"):
            n = clear_cache()
            st.success(f"Cleared {n} cached entries.")

    st.divider()
    all_results_sidebar = st.session_state.get("brand_results", []) + st.session_state.get("unbranded_results", [])
    if all_results_sidebar:
        st.markdown("### 📦 Export")
        st.download_button(
            "⬇ Download Combined CSV",
            results_to_csv(all_results_sidebar),
            "ai_audit_combined.csv", "text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    st.caption("AI Visibility Audit v2.1")


# ─────────────────────────────────────────────
# Resolve active providers (used throughout)
# ─────────────────────────────────────────────
def get_providers():
    p = []
    if openai_key:
        p.append(("OpenAI", openai_key, openai_model))
    if gemini_key:
        p.append(("Gemini", gemini_key, gemini_model))
    if perplexity_key:
        p.append(("Perplexity", perplexity_key, perplexity_model))
    return p


def first_provider_for_recs(industry_val, country_val):
    """Returns (name, key, model, industry, country) for fix-it recommendations."""
    for name, key, model in get_providers():
        return (name, key, model, industry_val, country_val)
    return None


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">GEO Audit Tool</div>
    <h1>AI Visibility &amp; Discovery Audit</h1>
    <p>Measure how AI models perceive, rank, and recommend your brand — and where competitors have the edge.</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SHARED INPUTS
# ─────────────────────────────────────────────
st.markdown("### 🏢 Client & Context Setup")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    # Feature 1: pre-fill from loaded profile
    loaded = st.session_state.get("_loaded_profile", {})
    client_name = st.text_input("Client / Brand Name",
        value=loaded.get("client_name", ""),
        placeholder="e.g. Acme Corp")
    website_url = st.text_input("Website URL",
        value=loaded.get("website_url", ""),
        placeholder="https://www.acme.com")

with col2:
    if st.button("🔍 Auto-detect Industry", use_container_width=True):
        providers_now = get_providers()
        if website_url and providers_now:
            with st.spinner("Crawling website…"):
                _, text = get_links(website_url)
                pn, pk, pm = providers_now[0]
                res = query_llm(pn, pk,
                    f"Based on this website text, identify the specific industry and primary core service. "
                    f"Return ONLY in this format: Industry | Service\n\n{text[:2500]}",
                    model=pm)
                if "|" in res.get("text", ""):
                    ind, svc = [x.strip() for x in res["text"].split("|", 1)]
                    st.session_state["industry"] = ind
                    st.session_state["service"] = svc
                    st.session_state["last_url"] = website_url
                    st.success(f"Detected: **{ind}** — *{svc}*")
                elif res.get("error"):
                    st.error(res["error"])
        else:
            st.warning("Enter a website URL and at least one API key first.")

    industry = st.text_input("Industry",
        value=st.session_state.get("industry", loaded.get("industry", "")),
        placeholder="e.g. financial services")
    core_service = st.text_input("Core Service",
        value=st.session_state.get("service", loaded.get("core_service", "")),
        placeholder="e.g. wealth management")

with col3:
    default_comps = "\n".join(loaded.get("competitors", []))
    competitor_input = st.text_area("Competitors (1 per line, max 5)",
        value=default_comps,
        placeholder="Competitor A\nCompetitor B",
        height=140)
    competitors = [c.strip() for c in competitor_input.split("\n") if c.strip()][:5]

# ── Feature 1: handle pending save ───────────
if st.session_state.get("_pending_save"):
    save_name = st.session_state.pop("_pending_save")
    if client_name:
        save_profile(save_name, profile_to_dict(
            client_name, website_url, industry, core_service,
            competitors, country, openai_model, gemini_model, perplexity_model,
        ))
        st.success(f"Profile '{save_name}' saved.")
    else:
        st.warning("Enter a client name before saving.")

st.divider()


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏷 Brand Audit",
    "🌐 Unbranded Audit",
    "📊 Combined Dashboard",
    "✏️ Question Editor",   # Feature 9
])


# ─────────────────────────────────────────────
# Shared run helper
# ─────────────────────────────────────────────
def run_tasks(all_tasks: list, label: str) -> list:
    """Execute a list of query tasks with progress bar. Returns results list."""
    st.info(f"Running {len(all_tasks)} {label} queries across {len(get_providers())} provider(s)…")
    progress_bar = st.progress(0)
    status_text = st.empty()
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_audit_query, t[0], t[1], t[2], t[3], t[4],
                            t[5], t[6], t[7], t[8], use_cache): i
            for i, t in enumerate(all_tasks)
        }
        completed = 0
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({"Error": str(e), "Question": "Unknown", "Provider": "Unknown",
                                 "Category": "Error", "Funnel Stage": "", "Audience": "",
                                 "Goal": "", "Model": "", "Response": "", "Sentiment": "Neutral",
                                 "GEO Score": "5", "Hallucination Risk": "Low", "Key Entities": "",
                                 "Client Mentioned": "No", "Client Mention Count": 0,
                                 "Competitor Mentions": "", "Competitor Mention Counts": "{}",
                                 "Citations": "[]", "_from_cache": False})
            completed += 1
            progress_bar.progress(completed / len(all_tasks))
            status_text.caption(f"Completed {completed} / {len(all_tasks)}")
    status_text.empty()
    return results


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

    bcol1, bcol2 = st.columns(2)
    selected_cats = []
    for i, cat in enumerate(BRANDED_CATEGORIES.keys()):
        col = bcol1 if i % 2 == 0 else bcol2
        # Feature 9: include extra questions in count
        extra = st.session_state["custom_branded_q"].get(cat, [])
        total_q = len(BRANDED_CATEGORIES[cat]) + len(extra)
        if col.checkbox(f"{cat} ({total_q} questions)", key=f"branded_cat_{cat}"):
            selected_cats.append(cat)

    custom_questions_input = st.text_area(
        "Ad-hoc Custom Questions (1 per line)",
        placeholder="How does {client} handle {industry} regulations?\nIs {client} better than {competitors}?",
        help="Use {client}, {industry}, {service}, {competitors} as placeholders.",
        height=80,
    )
    custom_questions = [q.strip() for q in custom_questions_input.split("\n") if q.strip()]

    run_brand = st.button("▶ Run Brand Audit", type="primary")

    if run_brand:
        providers = get_providers()
        if not providers:
            st.error("Add at least one API key in the sidebar.")
        elif not client_name:
            st.error("Enter a Client Name above.")
        elif not selected_cats and not custom_questions:
            st.warning("Select at least one category or add a custom question.")
        else:
            all_tasks = []
            for cat in selected_cats:
                # Built-in + Feature 9 custom questions merged
                base_qs = BRANDED_CATEGORIES[cat]
                extra_qs = [
                    {"funnel": "Custom", "audience": "General", "question": q, "goal": "Custom question (editor)"}
                    for q in st.session_state["custom_branded_q"].get(cat, [])
                ]
                for q_data in base_qs + extra_qs:
                    display_q = format_prompt(q_data["question"], client_name, competitors, country, industry, core_service)
                    for pn, pk, pm in providers:
                        all_tasks.append((pn, pk, display_q, q_data, cat, client_name, competitors, country, pm))

            for cq in custom_questions:
                display_q = cq.replace("{client}", client_name).replace("{competitors}", ", ".join(competitors)) \
                              .replace("{industry}", industry).replace("{service}", core_service)
                for pn, pk, pm in providers:
                    all_tasks.append((pn, pk, display_q, {}, "Custom", client_name, competitors, country, pm))

            brand_results = run_tasks(all_tasks, "branded")
            st.session_state["brand_results"] = brand_results
            st.success(f"Brand audit complete — {len(brand_results)} results.")

    if st.session_state.get("brand_results"):
        st.divider()
        st.markdown("### Brand Audit Results")
        prov_rec = first_provider_for_recs(industry, country)
        render_results_grid(st.session_state["brand_results"], client_name or "Your Brand", prov_rec)
        st.download_button("⬇ Download Brand Audit CSV",
            results_to_csv(st.session_state["brand_results"]), "brand_audit.csv", "text/csv")


# ─────────────────────────────────────────────
# TAB 2 — UNBRANDED AUDIT
# ─────────────────────────────────────────────
with tab2:
    st.markdown("#### Unbranded Visibility Audit")
    st.markdown(
        "<div class='info-box'>Ask LLMs generic industry questions <strong>without mentioning your brand</strong>. "
        "Brand mentions in responses count as earned AI share of voice.</div>",
        unsafe_allow_html=True,
    )

    uc1, uc2 = st.columns(2)
    selected_unbranded_cats = []
    for i, cat in enumerate(UNBRANDED_CATEGORIES.keys()):
        col = uc1 if i % 2 == 0 else uc2
        extra = st.session_state["custom_unbranded_q"].get(cat, [])
        total_q = len(UNBRANDED_CATEGORIES[cat]) + len(extra)
        if col.checkbox(f"{cat} ({total_q} questions)", value=True, key=f"unbranded_cat_{cat}"):
            selected_unbranded_cats.append(cat)

    st.markdown("##### Keyword Discovery")
    kw_col1, kw_col2 = st.columns(2)
    with kw_col1:
        manual_keywords = st.text_area("Manual Keywords (1 per line)", height=90,
            placeholder="wealth management\nfinancial planning")
    with kw_col2:
        use_auto_keywords = st.checkbox("Auto-generate keywords from website", value=True)
        kw_count = st.slider("Keywords to generate", 3, 10, 5)

    run_unbranded = st.button("▶ Run Unbranded Audit", type="primary", key="run_unbranded_btn")

    if run_unbranded:
        providers = get_providers()
        if not providers:
            st.error("Add at least one API key in the sidebar.")
        elif not client_name:
            st.error("Enter a Client Name above.")
        else:
            pn_kw, pk_kw, pm_kw = providers[0]

            with st.status("Running Unbranded Audit…", expanded=True) as status:
                all_unbranded_tasks = []

                for cat in selected_unbranded_cats:
                    base_qs = UNBRANDED_CATEGORIES[cat]
                    extra_qs = [
                        {"funnel": "Custom", "audience": "General", "question": q, "goal": "Custom question (editor)"}
                        for q in st.session_state["custom_unbranded_q"].get(cat, [])
                    ]
                    for q_data in base_qs + extra_qs:
                        display_q = format_prompt(q_data["question"], client_name, competitors, country, industry, core_service)
                        for pn, pk, pm in providers:
                            all_unbranded_tasks.append((pn, pk, display_q, q_data, cat, client_name, competitors, country, pm))

                if use_auto_keywords or manual_keywords.strip():
                    st.write("Gathering keywords…")
                    keywords = [k.strip() for k in manual_keywords.split("\n") if k.strip()]

                    if use_auto_keywords and website_url:
                        links, home_text = get_links(website_url)
                        combined_text = home_text
                        for link in links[:3]:
                            _, sub_text = get_links(link)
                            combined_text += " " + sub_text
                        kw_res = query_llm(pn_kw, pk_kw,
                            f"Context: {country}, Industry: {industry}. "
                            f"Identify {kw_count} unbranded SEO keywords for {core_service or 'services in this industry'}. "
                            f"Return ONLY keywords, one per line:\n\n{combined_text[:4000]}",
                            model=pm_kw)
                        if not kw_res.get("error"):
                            auto_kws = [k.strip() for k in kw_res["text"].split("\n") if k.strip()][:kw_count]
                            keywords = list(dict.fromkeys(keywords + auto_kws))

                    if keywords:
                        st.write(f"Keywords: **{', '.join(keywords)}**")
                        for kw in keywords:
                            q_res = query_llm(pn_kw, pk_kw,
                                f"Context: {country}, Industry: {industry}. "
                                f"Generate 3 unbranded questions a user might ask about '{kw}'. "
                                f"Return ONLY questions, one per line.", model=pm_kw)
                            if not q_res.get("error"):
                                for q in [x.strip() for x in q_res["text"].split("\n") if x.strip()][:3]:
                                    for pn, pk, pm in providers:
                                        all_unbranded_tasks.append((
                                            pn, pk, q,
                                            {"funnel": "Discovery", "goal": f"Keyword: {kw}", "audience": "General"},
                                            "Keyword Discovery", client_name, competitors, country, pm
                                        ))

                status.update(label=f"Querying {len(all_unbranded_tasks)} questions…", state="running")
                pb = st.progress(0)
                unbranded_results = []
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futs = {
                        executor.submit(run_audit_query, t[0], t[1], t[2], t[3], t[4],
                                        t[5], t[6], t[7], t[8], use_cache): i
                        for i, t in enumerate(all_unbranded_tasks)
                    }
                    done = 0
                    for future in as_completed(futs):
                        try:
                            unbranded_results.append(future.result())
                        except Exception:
                            pass
                        done += 1
                        pb.progress(done / len(all_unbranded_tasks))

                st.session_state["unbranded_results"] = unbranded_results
                status.update(label=f"Complete — {len(unbranded_results)} results.", state="complete")

    if st.session_state.get("unbranded_results"):
        st.divider()
        st.markdown("### Unbranded Audit Results")
        prov_rec = first_provider_for_recs(industry, country)
        render_results_grid(st.session_state["unbranded_results"], client_name or "Your Brand", prov_rec)
        st.download_button("⬇ Download Unbranded Audit CSV",
            results_to_csv(st.session_state["unbranded_results"]), "unbranded_audit.csv", "text/csv")


# ─────────────────────────────────────────────
# TAB 3 — COMBINED DASHBOARD
# ─────────────────────────────────────────────
with tab3:
    brand_res = st.session_state.get("brand_results", [])
    unbranded_res = st.session_state.get("unbranded_results", [])
    all_res = brand_res + unbranded_res

    if not all_res:
        st.info("Run a Brand Audit and/or Unbranded Audit to populate this dashboard.")
    else:
        st.markdown("### Combined Audit Dashboard")
        df_all = pd.DataFrame(all_res)
        total = len(df_all)
        mentioned = (df_all["Client Mentioned"] == "Yes").sum()
        geo_avg = pd.to_numeric(df_all["GEO Score"], errors="coerce").mean()
        error_count = (df_all.get("Error", pd.Series([""] * total)) != "").sum()

        # ── Citation summary (Feature 12) ─────
        all_citations = []
        for r in all_res:
            try:
                all_citations.extend(json.loads(r.get("Citations", "[]")))
            except Exception:
                pass
        unique_citations = list(dict.fromkeys(all_citations))

        d1, d2, d3, d4, d5 = st.columns(5)
        d1.metric("Total Queries", total)
        d2.metric("Overall Brand SOV", f"{mentioned/total*100:.1f}%" if total else "N/A")
        d3.metric("Avg GEO Score", f"{geo_avg:.1f}/10" if not pd.isna(geo_avg) else "N/A")
        d4.metric("Failed Queries", int(error_count))
        d5.metric("Unique Citations Found", len(unique_citations),
                  help="Total unique URLs cited by Perplexity or embedded in other responses (Feature 12)")

        st.divider()

        dcol1, dcol2 = st.columns(2)

        with dcol1:
            b_mentioned = sum(1 for r in brand_res if r.get("Client Mentioned") == "Yes") if brand_res else 0
            u_mentioned = sum(1 for r in unbranded_res if r.get("Client Mentioned") == "Yes") if unbranded_res else 0
            sov_compare = pd.DataFrame({
                "Audit Type": ["Brand Audit", "Unbranded Audit"],
                "SOV %": [
                    (b_mentioned / len(brand_res) * 100) if brand_res else 0,
                    (u_mentioned / len(unbranded_res) * 100) if unbranded_res else 0,
                ],
            })
            fig_sov = px.bar(sov_compare, x="Audit Type", y="SOV %",
                             title="Brand SOV by Audit Type", color="Audit Type",
                             color_discrete_sequence=["#2563eb", "#06b6d4"])
            fig_sov.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", title_font_size=13, showlegend=False,
                margin=dict(t=40, b=0, l=0, r=0),
                yaxis=dict(gridcolor="#2d3748", range=[0, 100]),
                xaxis=dict(gridcolor="#2d3748"),
            )
            st.plotly_chart(fig_sov, use_container_width=True)

        with dcol2:
            if "Provider" in df_all.columns:
                sent_prov = df_all.groupby(["Provider", "Sentiment"]).size().reset_index(name="Count")
                fig_sp = px.bar(sent_prov, x="Provider", y="Count", color="Sentiment",
                                title="Sentiment by Provider",
                                color_discrete_map={"Positive": "#22c55e", "Neutral": "#60a5fa", "Negative": "#ef4444"},
                                barmode="stack")
                fig_sp.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0", title_font_size=13,
                    margin=dict(t=40, b=0, l=0, r=0),
                    yaxis=dict(gridcolor="#2d3748"), xaxis=dict(gridcolor="#2d3748"),
                    legend=dict(font=dict(color="#94a3b8")),
                )
                st.plotly_chart(fig_sp, use_container_width=True)

        # ── Feature 12: citation breakdown ────
        if unique_citations:
            st.divider()
            st.markdown("#### Citation Sources Found")
            st.markdown(
                "<div class='info-box'>These URLs were cited by Perplexity or embedded in responses. "
                "High-frequency domains indicate which sources AI models consider authoritative for your industry.</div>",
                unsafe_allow_html=True,
            )
            from urllib.parse import urlparse as _up
            domain_counts: dict[str, int] = {}
            for url in all_citations:
                try:
                    d = _up(url).netloc.replace("www.", "")
                    domain_counts[d] = domain_counts.get(d, 0) + 1
                except Exception:
                    pass
            if domain_counts:
                domain_df = pd.DataFrame(
                    sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:20],
                    columns=["Domain", "Citations"]
                )
                fig_cit = px.bar(domain_df, x="Citations", y="Domain", orientation="h",
                                 title="Top Cited Domains",
                                 color="Citations",
                                 color_continuous_scale=["#1e3a5f", "#2563eb", "#60a5fa"])
                fig_cit.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0", title_font_size=13, coloraxis_showscale=False,
                    margin=dict(t=40, b=0, l=0, r=0),
                    xaxis=dict(gridcolor="#2d3748"), yaxis=dict(gridcolor="#2d3748"),
                )
                st.plotly_chart(fig_cit, use_container_width=True)

            with st.expander("All citation URLs"):
                for url in unique_citations:
                    st.markdown(f"- [{url}]({url})")

        st.divider()
        st.markdown("#### Full Results Table")
        display_cols = ["Category", "Funnel Stage", "Provider", "Model", "Sentiment",
                        "GEO Score", "Hallucination Risk", "Client Mentioned", "Competitor Mentions", "Question"]
        available_cols = [c for c in display_cols if c in df_all.columns]
        st.dataframe(df_all[available_cols], use_container_width=True, hide_index=True,
                     column_config={
                         "GEO Score": st.column_config.NumberColumn(format="%d/10"),
                         "Question": st.column_config.TextColumn(width="large"),
                     })
        st.download_button("⬇ Download Full Combined CSV",
            results_to_csv(all_res), "ai_audit_full.csv", "text/csv")


# ─────────────────────────────────────────────
# TAB 4 — QUESTION EDITOR (Feature 9)
# ─────────────────────────────────────────────
with tab4:
    st.markdown("#### Question Editor")
    st.markdown(
        "<div class='info-box'>Add, preview, or disable questions per category without editing any code. "
        "Custom questions are saved to session state and included in the next audit run.</div>",
        unsafe_allow_html=True,
    )

    editor_type = st.radio("Edit questions for:", ["Branded", "Unbranded"], horizontal=True)
    cat_dict = BRANDED_CATEGORIES if editor_type == "Branded" else UNBRANDED_CATEGORIES
    custom_key = "custom_branded_q" if editor_type == "Branded" else "custom_unbranded_q"

    cat_sel = st.selectbox("Select category to edit", list(cat_dict.keys()), key="editor_cat_sel")

    if cat_sel:
        built_in_qs = cat_dict[cat_sel]
        custom_qs = st.session_state[custom_key].get(cat_sel, [])

        st.markdown(f"**Built-in questions ({len(built_in_qs)})** — read-only")
        for i, q in enumerate(built_in_qs):
            with st.expander(f"{i+1}. {q['question'][:80]}…" if len(q['question']) > 80 else f"{i+1}. {q['question']}"):
                c1, c2 = st.columns(2)
                c1.markdown(f"**Funnel:** {q['funnel']}")
                c1.markdown(f"**Audience:** {q['audience']}")
                c2.markdown(f"**Goal:** {q['goal']}")

        st.divider()
        st.markdown(f"**Your custom questions for '{cat_sel}'** ({len(custom_qs)} added)")

        if custom_qs:
            to_delete = []
            for i, cq in enumerate(custom_qs):
                cc1, cc2 = st.columns([5, 1])
                cc1.markdown(f"`{cq}`")
                if cc2.button("Remove", key=f"remove_cq_{editor_type}_{cat_sel}_{i}"):
                    to_delete.append(i)
            if to_delete:
                updated = [q for j, q in enumerate(custom_qs) if j not in to_delete]
                st.session_state[custom_key][cat_sel] = updated
                st.rerun()

        new_q = st.text_area(
            "Add new custom questions (1 per line)",
            placeholder=(
                "How does {client} compare to {competitors} on customer support?\n"
                "What is {client}'s approach to innovation in {industry}?"
            ),
            height=100,
            key=f"new_q_input_{editor_type}_{cat_sel}",
        )
        if st.button("➕ Add to category", key=f"add_q_btn_{editor_type}_{cat_sel}"):
            new_list = [q.strip() for q in new_q.split("\n") if q.strip()]
            if new_list:
                existing = st.session_state[custom_key].get(cat_sel, [])
                st.session_state[custom_key][cat_sel] = existing + new_list
                st.success(f"Added {len(new_list)} question(s) to '{cat_sel}'.")
                st.rerun()

        if st.button("🗑 Clear all custom questions for this category",
                     key=f"clear_cat_{editor_type}_{cat_sel}"):
            st.session_state[custom_key][cat_sel] = []
            st.success("Cleared.")
            st.rerun()

    st.divider()
    st.markdown("#### All Custom Questions Summary")
    branded_total = sum(len(v) for v in st.session_state["custom_branded_q"].values())
    unbranded_total = sum(len(v) for v in st.session_state["custom_unbranded_q"].values())
    sc1, sc2 = st.columns(2)
    sc1.metric("Custom Branded Questions", branded_total)
    sc2.metric("Custom Unbranded Questions", unbranded_total)

    if st.button("🗑 Clear ALL custom questions", key="clear_all_custom"):
        st.session_state["custom_branded_q"] = {}
        st.session_state["custom_unbranded_q"] = {}
        st.success("All custom questions cleared.")
        st.rerun()

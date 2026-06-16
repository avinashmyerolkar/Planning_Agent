import streamlit as st
from graphs.blog_graph import build_graph

st.set_page_config(
    page_title="Quill — AI Content Engine",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] { background: #FAFAFA; }
[data-testid="stHeader"]           { background: transparent; }
[data-testid="stSidebar"]          { display: none; }
.block-container                   { max-width: 780px; padding: 2.5rem 2rem 6rem; }
#MainMenu, footer, header          { visibility: hidden; }

/* ── Brand ── */
.quill-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 3rem;
}
.quill-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}
.quill-mark {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 800; color: white;
    letter-spacing: -1px;
    flex-shrink: 0;
}
.quill-wordmark {
    font-size: 1.1rem;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.02em;
}
.quill-version {
    font-size: 0.68rem;
    font-weight: 600;
    color: #7C3AED;
    background: #F5F3FF;
    padding: 2px 8px;
    border-radius: 100px;
    border: 1px solid #DDD6FE;
}

/* ── Hero ── */
.hero {
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #7C3AED;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
}
.hero-eyebrow-dot {
    width: 6px; height: 6px;
    background: #7C3AED;
    border-radius: 50%;
    display: inline-block;
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.04em;
    line-height: 1.15;
    margin-bottom: 1rem;
}
.hero-title span {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1rem;
    color: #6B7280;
    line-height: 1.65;
    max-width: 560px;
}

/* ── Pipeline bar ── */
.pipeline-bar {
    display: flex;
    align-items: center;
    gap: 0;
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 10px 16px;
    margin: 1.75rem 0;
    width: fit-content;
}
.pipe-step {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #374151;
    padding: 0 10px;
}
.pipe-step:first-child { padding-left: 0; }
.pipe-icon {
    width: 22px; height: 22px;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px;
}
.pipe-icon-orch  { background: #EEF2FF; color: #4F46E5; }
.pipe-icon-work  { background: #F0FDF4; color: #16A34A; }
.pipe-icon-red   { background: #FFF7ED; color: #EA580C; }
.pipe-arrow {
    color: #D1D5DB;
    font-size: 0.7rem;
    padding: 0 2px;
}

/* ── Input card ── */
.input-card {
    background: white;
    border: 1.5px solid #E5E7EB;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.03);
}
.input-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.6rem;
}

/* ── Textarea ── */
.stTextArea label { display: none !important; }
.stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid #E5E7EB !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    color: #111827 !important;
    background: #FAFAFA !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
    resize: none !important;
}
.stTextArea textarea::placeholder { color: #9CA3AF !important; }
.stTextArea textarea:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
    background: white !important;
    outline: none !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: all 0.15s ease !important;
    border: none !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    color: white !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 2px 8px rgba(79,70,229,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(79,70,229,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"]:disabled {
    background: #E5E7EB !important;
    color: #9CA3AF !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Progress ── */
.stProgress > div > div {
    background: #F3F4F6 !important;
    border-radius: 100px !important;
    height: 6px !important;
}
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    border-radius: 100px !important;
}

/* ── Status widget ── */
[data-testid="stStatusWidget"] {
    border-radius: 14px !important;
    border: 1.5px solid #E5E7EB !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 1.1rem 1.25rem 0.9rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
[data-testid="stMetricLabel"]  { color: #6B7280 !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
[data-testid="stMetricValue"]  { color: #111827 !important; font-size: 1.6rem !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }
[data-testid="stMetricDelta"]  { display: none; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #F3F4F6 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
    border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 500 !important;
    color: #6B7280 !important;
    border: none !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #111827 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    border-radius: 10px !important;
    border: 1.5px solid #E5E7EB !important;
    background: white !important;
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    border-color: #7C3AED !important;
    color: #7C3AED !important;
    background: #FAFAFF !important;
}

/* ── Section cards in outline ── */
.section-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #F9FAFB;
}
.section-row:last-child { border-bottom: none; }
.section-num {
    min-width: 26px; height: 26px;
    background: #F3F4F6;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    color: #6B7280;
    margin-top: 1px;
}
.section-title  { font-size: 0.88rem; font-weight: 600; color: #111827; }
.section-brief  { font-size: 0.8rem; color: #6B7280; margin-top: 1px; line-height: 1.4; }

/* ── Expander ── */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    color: #374151 !important;
    font-size: 0.88rem !important;
}

/* ── Result header ── */
.result-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 2rem 0 1.25rem;
}
.result-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #F0FDF4;
    color: #16A34A;
    border: 1px solid #BBF7D0;
    border-radius: 100px;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
}
.result-title {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
}

hr { border: none; border-top: 1px solid #F3F4F6 !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Nav ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="quill-nav">
    <div class="quill-logo">
        <div class="quill-mark">Q</div>
        <span class="quill-wordmark">Quill</span>
    </div>
    <span class="quill-version">Beta</span>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">
        <span class="hero-eyebrow-dot"></span>
        Multi-agent content engine
    </div>
    <div class="hero-title">
        From idea to article,<br><span>written by agents.</span>
    </div>
    <div class="hero-sub">
        Quill plans your article, dispatches parallel AI writers for each section,
        then assembles a polished draft — all in a single run.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline visualization ─────────────────────────────────────────────────────
st.markdown("""
<div class="pipeline-bar">
    <div class="pipe-step">
        <div class="pipe-icon pipe-icon-orch">◆</div>
        Orchestrator
    </div>
    <span class="pipe-arrow">›</span>
    <div class="pipe-step">
        <div class="pipe-icon pipe-icon-work">⚡</div>
        Workers <span style="color:#9CA3AF;font-weight:400">&nbsp;(parallel)</span>
    </div>
    <span class="pipe-arrow">›</span>
    <div class="pipe-step">
        <div class="pipe-icon pipe-icon-red">⬡</div>
        Reducer
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-label">Article topic</div>', unsafe_allow_html=True)

topic = st.text_area(
    "topic",
    placeholder='e.g.  "How Self-Attention Works in Transformers"',
    height=96,
    label_visibility="collapsed",
)

col_btn, col_hint = st.columns([2, 4])
with col_btn:
    generate = st.button(
        "Generate article  →",
        type="primary",
        disabled=not topic.strip(),
        use_container_width=True,
    )
with col_hint:
    if topic.strip():
        wc = len(topic.split())
        st.caption(f"**{wc}** {'word' if wc == 1 else 'words'} · ready to generate")
    else:
        st.caption("Describe your topic above to get started")

# ── Pipeline execution ─────────────────────────────────────────────────────────
if generate and topic.strip():
    for key in ["final_blog", "plan"]:
        st.session_state.pop(key, None)

    app = build_graph()
    plan = None
    total_sections = 0
    sections_done = 0

    st.markdown("<br>", unsafe_allow_html=True)

    with st.status("Running Quill pipeline…", expanded=True) as status:
        progress = st.progress(0.0, text="Orchestrator is planning…")

        for event in app.stream({"topic": topic.strip()}, stream_mode="updates"):
            for node, output in event.items():

                if node == "orchestrator":
                    plan = output["plan"]
                    total_sections = len(plan.tasks)
                    st.session_state.plan = plan

                    st.markdown(
                        f"<p style='margin:0 0 8px;font-size:0.88rem;'>"
                        f"<strong>Outline locked</strong> · "
                        f"<em style='color:#6B7280'>{plan.blog_title}</em>"
                        f"</p>",
                        unsafe_allow_html=True,
                    )
                    with st.expander(f"{total_sections} sections planned — view outline"):
                        for t in plan.tasks:
                            brief = t.brief[:95] + ("…" if len(t.brief) > 95 else "")
                            st.markdown(
                                f"<div class='section-row'>"
                                f"<div class='section-num'>{t.id:02d}</div>"
                                f"<div>"
                                f"<div class='section-title'>{t.title}</div>"
                                f"<div class='section-brief'>{brief}</div>"
                                f"</div></div>",
                                unsafe_allow_html=True,
                            )
                    progress.progress(0.1, text=f"Dispatching workers…  0 / {total_sections}")

                elif node == "worker":
                    sections_done += 1
                    frac = 0.1 + 0.85 * (sections_done / max(total_sections, 1))
                    progress.progress(
                        frac,
                        text=f"Writing sections…  {sections_done} / {total_sections}",
                    )
                    st.markdown(
                        f"<p style='margin:2px 0;font-size:0.84rem;color:#374151;'>"
                        f"<span style='color:#16A34A;font-weight:700;'>✓</span>&nbsp;"
                        f"Section {sections_done} of {total_sections} complete</p>",
                        unsafe_allow_html=True,
                    )

                elif node == "reducer":
                    st.session_state.final_blog = output["final"]
                    st.session_state.blog_title = plan.blog_title if plan else "article"
                    progress.progress(1.0, text="Assembly complete")

        status.update(label="Article ready", state="complete", expanded=False)

# ── Output ─────────────────────────────────────────────────────────────────────
if "final_blog" in st.session_state:
    blog = st.session_state.final_blog
    safe_title = st.session_state.get("blog_title", "article").lower().replace(" ", "_")
    plan = st.session_state.get("plan")

    st.markdown("""
    <div class="result-header">
        <span class="result-badge">✓ &nbsp;Complete</span>
        <span class="result-title">Your article is ready</span>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Words", f"{len(blog.split()):,}")
    with c2:
        st.metric("Sections", len(plan.tasks) if plan else "—")
    with c3:
        st.metric("Characters", f"{len(blog):,}")

    st.markdown("<br>", unsafe_allow_html=True)

    dl_col, _, __ = st.columns([2, 2, 3])
    with dl_col:
        st.download_button(
            "⬇  Download .md",
            data=blog,
            file_name=f"{safe_title}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tab_preview, tab_raw = st.tabs(["Preview", "Markdown"])
    with tab_preview:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(blog)
    with tab_raw:
        st.code(blog, language="markdown", line_numbers=True)

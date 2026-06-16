import streamlit as st
from graphs.blog_graph import build_graph

st.set_page_config(
    page_title="Quill — AI Content Engine",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header   { visibility: hidden; }

/* ── Page background ── */
[data-testid="stAppViewContainer"] { background: #F0EFF8; }
[data-testid="stHeader"]            { display: none; }
[data-testid="stSidebar"]           { display: none; }
.block-container                    { padding: 1.5rem 1.75rem !important; max-width: 100% !important; }

/* ── Two-panel cards ── */
div[data-testid="column"]:first-child {
    background: white;
    border-radius: 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    padding: 1.75rem 1.5rem !important;
    position: sticky;
    top: 1.5rem;
    align-self: flex-start;
    max-height: calc(100vh - 3rem);
    overflow-y: auto;
}
div[data-testid="column"]:last-child {
    background: white;
    border-radius: 18px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    padding: 1.75rem 2rem !important;
    min-height: calc(100vh - 3rem);
}

/* ── Scrollbar ── */
div[data-testid="column"]:first-child::-webkit-scrollbar { width: 4px; }
div[data-testid="column"]:first-child::-webkit-scrollbar-track { background: transparent; }
div[data-testid="column"]:first-child::-webkit-scrollbar-thumb { background: #E5E7EB; border-radius: 4px; }

/* ── Brand ── */
.brand {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
}
.brand-left { display: flex; align-items: center; gap: 9px; }
.brand-mark {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 800; color: white;
    flex-shrink: 0;
}
.brand-name  { font-size: 1rem; font-weight: 700; color: #111827; letter-spacing: -0.02em; }
.brand-badge {
    font-size: 0.65rem; font-weight: 600;
    color: #7C3AED; background: #F5F3FF;
    border: 1px solid #DDD6FE;
    padding: 2px 7px; border-radius: 100px;
}

/* ── Section label ── */
.field-label {
    font-size: 0.72rem; font-weight: 600;
    color: #374151; text-transform: uppercase;
    letter-spacing: 0.07em; margin-bottom: 0.5rem;
}

/* ── Textarea ── */
.stTextArea label { display: none !important; }
.stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid #E5E7EB !important;
    font-size: 0.9rem !important;
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
    font-size: 0.85rem !important;
    border: none !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(79,70,229,0.3) !important;
    padding: 0.55rem 1.25rem !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 5px 18px rgba(79,70,229,0.45) !important;
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
    background: #F3F4F6 !important; border-radius: 100px !important; height: 5px !important;
}
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #4F46E5, #7C3AED) !important; border-radius: 100px !important;
}

/* ── Status widget ── */
[data-testid="stStatusWidget"] { border-radius: 12px !important; border: 1px solid #E5E7EB !important; }

/* ── Divider ── */
hr { border: none !important; border-top: 1px solid #F3F4F6 !important; margin: 1.25rem 0 !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #FAFAFA; border: 1px solid #F3F4F6;
    border-radius: 12px; padding: 0.85rem 1rem 0.7rem !important;
}
[data-testid="stMetricLabel"] { color: #9CA3AF !important; font-size: 0.7rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
[data-testid="stMetricValue"] { color: #111827 !important; font-size: 1.4rem !important; font-weight: 700 !important; letter-spacing: -0.02em !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #F3F4F6 !important; border-radius: 10px !important;
    padding: 3px !important; gap: 2px !important; border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important; font-weight: 500 !important;
    color: #6B7280 !important; border: none !important;
    font-size: 0.82rem !important; padding: 0.35rem 0.9rem !important;
}
.stTabs [aria-selected="true"] {
    background: white !important; color: #111827 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    border-radius: 9px !important; border: 1.5px solid #E5E7EB !important;
    background: white !important; color: #374151 !important;
    font-weight: 600 !important; font-size: 0.82rem !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    border-color: #7C3AED !important; color: #7C3AED !important;
}

/* ── Expander ── */
.streamlit-expanderHeader { font-weight: 600 !important; color: #374151 !important; font-size: 0.83rem !important; }

/* ── Empty state ── */
.empty-state {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: calc(100vh - 10rem);
    text-align: center; color: #9CA3AF;
}
.empty-icon {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #EEF2FF, #F5F3FF);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; margin-bottom: 1rem;
    border: 1px solid #E0E7FF;
}
.empty-title { font-size: 1rem; font-weight: 600; color: #374151; margin-bottom: 0.35rem; }
.empty-sub   { font-size: 0.82rem; color: #9CA3AF; line-height: 1.5; max-width: 240px; }

/* ── Step list in left panel ── */
.step-item {
    display: flex; align-items: flex-start; gap: 9px;
    padding: 5px 0; font-size: 0.82rem;
}
.step-dot-pending { width: 8px; height: 8px; border-radius: 50%; background: #E5E7EB; margin-top: 4px; flex-shrink: 0; }
.step-dot-active  { width: 8px; height: 8px; border-radius: 50%; background: #7C3AED; margin-top: 4px; flex-shrink: 0; box-shadow: 0 0 0 3px rgba(124,58,237,0.2); }
.step-dot-done    { width: 8px; height: 8px; border-radius: 50%; background: #10B981; margin-top: 4px; flex-shrink: 0; }
.step-text-muted  { color: #9CA3AF; }
.step-text-active { color: #7C3AED; font-weight: 600; }
.step-text-done   { color: #374151; font-weight: 500; }

/* ── Section outline row ── */
.outline-row {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 7px 0; border-bottom: 1px solid #F9FAFB;
    font-size: 0.8rem;
}
.outline-row:last-child { border-bottom: none; }
.outline-num {
    min-width: 22px; height: 22px; background: #F3F4F6;
    border-radius: 5px; display: flex; align-items: center;
    justify-content: center; font-size: 0.68rem; font-weight: 700;
    color: #6B7280; margin-top: 1px; flex-shrink: 0;
}
.outline-title { font-weight: 600; color: #111827; line-height: 1.3; }
.outline-brief { color: #6B7280; font-size: 0.75rem; margin-top: 1px; line-height: 1.35; }

/* ── Result badge ── */
.result-bar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.25rem;
}
.result-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: #F0FDF4; color: #16A34A;
    border: 1px solid #BBF7D0; border-radius: 100px;
    padding: 3px 10px; font-size: 0.72rem; font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ── Layout ─────────────────────────────────────────────────────────────────────
left, right = st.columns([4, 7], gap="medium")

# ══════════════════════════════════════════════════════════════════
# LEFT PANEL — input + pipeline status
# ══════════════════════════════════════════════════════════════════
with left:
    # Brand
    st.markdown("""
    <div class="brand">
        <div class="brand-left">
            <div class="brand-mark">Q</div>
            <span class="brand-name">Quill</span>
        </div>
        <span class="brand-badge">Beta</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Topic input
    st.markdown('<div class="field-label">Article topic</div>', unsafe_allow_html=True)
    topic = st.text_area(
        "topic",
        placeholder='e.g. "How Self-Attention Works in Transformers"',
        height=110,
        label_visibility="collapsed",
    )

    generate = st.button(
        "Generate article  →",
        type="primary",
        disabled=not topic.strip(),
        use_container_width=True,
    )

    if topic.strip():
        wc = len(topic.split())
        st.caption(f"{wc} {'word' if wc == 1 else 'words'}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Pipeline steps placeholder
    pipeline_area = st.empty()

    # Metrics placeholder (shown after generation)
    metrics_area = st.empty()

    # Show outline placeholder (shown after orchestrator)
    outline_area = st.empty()

# ══════════════════════════════════════════════════════════════════
# RIGHT PANEL — output
# ══════════════════════════════════════════════════════════════════
with right:
    output_area = st.empty()

    # Default empty state
    if "final_blog" not in st.session_state:
        output_area.markdown("""
        <div class="empty-state">
            <div class="empty-icon">◆</div>
            <div class="empty-title">Your article will appear here</div>
            <div class="empty-sub">Enter a topic on the left and click Generate to get started.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# GENERATION PIPELINE
# ══════════════════════════════════════════════════════════════════
if generate and topic.strip():
    for key in ["final_blog", "plan"]:
        st.session_state.pop(key, None)

    app = build_graph()
    plan = None
    total_sections = 0
    sections_done = 0

    def render_pipeline(plan=None, sections_done=0, total=0, done=False):
        lines = []
        # Step 1 — Orchestrator
        if plan:
            lines.append('<div class="step-item"><div class="step-dot-done"></div><span class="step-text-done">Outline ready</span></div>')
        else:
            lines.append('<div class="step-item"><div class="step-dot-active"></div><span class="step-text-active">Planning structure…</span></div>')

        # Step 2 — Workers
        if plan and not done:
            lines.append(
                f'<div class="step-item"><div class="step-dot-active"></div>'
                f'<span class="step-text-active">Writing sections&nbsp; {sections_done} / {total}</span></div>'
            )
        elif done:
            lines.append(f'<div class="step-item"><div class="step-dot-done"></div><span class="step-text-done">Sections written ({total})</span></div>')
        else:
            lines.append('<div class="step-item"><div class="step-dot-pending"></div><span class="step-text-muted">Write sections</span></div>')

        # Step 3 — Reducer
        if done:
            lines.append('<div class="step-item"><div class="step-dot-done"></div><span class="step-text-done">Article assembled</span></div>')
        else:
            lines.append('<div class="step-item"><div class="step-dot-pending"></div><span class="step-text-muted">Assemble article</span></div>')

        pipeline_area.markdown("".join(lines), unsafe_allow_html=True)

    render_pipeline()

    for event in app.stream({"topic": topic.strip()}, stream_mode="updates"):
        for node, output in event.items():

            if node == "orchestrator":
                plan = output["plan"]
                total_sections = len(plan.tasks)
                st.session_state.plan = plan

                render_pipeline(plan=plan, sections_done=0, total=total_sections)

                # Render outline in left panel
                rows = "".join(
                    f'<div class="outline-row">'
                    f'<div class="outline-num">{t.id:02d}</div>'
                    f'<div>'
                    f'<div class="outline-title">{t.title}</div>'
                    f'<div class="outline-brief">{t.brief[:70]}{"…" if len(t.brief) > 70 else ""}</div>'
                    f'</div></div>'
                    for t in plan.tasks
                )
                outline_area.markdown(
                    f'<div style="margin-top:0.25rem;font-size:0.72rem;font-weight:600;'
                    f'color:#9CA3AF;text-transform:uppercase;letter-spacing:0.07em;'
                    f'margin-bottom:0.6rem;">Outline</div>{rows}',
                    unsafe_allow_html=True,
                )

                # Clear right panel empty state
                output_area.empty()

            elif node == "worker":
                sections_done += 1
                render_pipeline(plan=plan, sections_done=sections_done, total=total_sections)

            elif node == "reducer":
                st.session_state.final_blog = output["final"]
                st.session_state.blog_title = plan.blog_title if plan else "article"
                render_pipeline(plan=plan, sections_done=total_sections, total=total_sections, done=True)

                # Metrics in left panel
                blog = output["final"]
                metrics_area.markdown(
                    f'<div style="margin-top:1rem;">'
                    f'<hr style="margin:1rem 0!important;">'
                    f'<div style="display:flex;gap:0.75rem;">'
                    f'<div style="flex:1;background:#FAFAFA;border:1px solid #F3F4F6;border-radius:10px;padding:0.7rem 0.85rem;">'
                    f'<div style="font-size:0.65rem;font-weight:600;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.05em;">Words</div>'
                    f'<div style="font-size:1.2rem;font-weight:700;color:#111827;letter-spacing:-0.02em;">{len(blog.split()):,}</div>'
                    f'</div>'
                    f'<div style="flex:1;background:#FAFAFA;border:1px solid #F3F4F6;border-radius:10px;padding:0.7rem 0.85rem;">'
                    f'<div style="font-size:0.65rem;font-weight:600;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.05em;">Sections</div>'
                    f'<div style="font-size:1.2rem;font-weight:700;color:#111827;letter-spacing:-0.02em;">{total_sections}</div>'
                    f'</div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

# ── Render final blog in right panel ──────────────────────────────
if "final_blog" in st.session_state:
    blog = st.session_state.final_blog
    safe_title = st.session_state.get("blog_title", "article").lower().replace(" ", "_")

    with right:
        # Header row
        dl_col, badge_col = st.columns([3, 2])
        with badge_col:
            st.markdown(
                '<div style="display:flex;justify-content:flex-end;padding-top:2px;">'
                '<span class="result-badge">✓ &nbsp;Complete</span></div>',
                unsafe_allow_html=True,
            )
        with dl_col:
            st.download_button(
                "⬇  Download .md",
                data=blog,
                file_name=f"{safe_title}.md",
                mime="text/markdown",
            )

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        tab_preview, tab_raw = st.tabs(["Preview", "Markdown"])
        with tab_preview:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            st.markdown(blog)
        with tab_raw:
            st.code(blog, language="markdown", line_numbers=True)

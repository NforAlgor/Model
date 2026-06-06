import streamlit as st
import pandas as pd
import pickle

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Productivity Analyzer",
    page_icon="\u25C8",
    layout="centered",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');

:root {
    --bg:          #f8fafc;
    --surface:     #ffffff;
    --surface2:    #f1f5f9;
    --border:      #e2e8f0;
    --accent:      #2563eb;
    --accent-glow: rgba(37,99,235,0.10);
    --text:        #1e293b;
    --muted:       #64748b;
    --white:       #0f172a;
    --success:     #059669;
    --warning:     #d97706;
    --danger:      #dc2626;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    background-color: var(--bg) !important;
    font-family: 'Sora', sans-serif !important;
    color: var(--text) !important;
}

[data-testid="block-container"] { padding-top: 2rem !important; }

/* hero */
.hero { text-align:center; padding:2.5rem 1rem 2rem; }
.hero-badge {
    display:inline-block;
    background:var(--accent-glow); border:1px solid var(--accent);
    color:var(--accent); font-size:0.7rem;
    font-family:'JetBrains Mono',monospace;
    letter-spacing:0.15em; padding:0.25rem 0.9rem;
    border-radius:999px; margin-bottom:1rem; text-transform:uppercase;
}
.hero h1 { font-size:2.4rem; font-weight:700; color:var(--white); line-height:1.15; margin:0 0 0.6rem; }
.hero h1 span { color:var(--accent); }
.hero p { color:var(--muted); font-size:0.95rem; max-width:480px; margin:0 auto; line-height:1.7; }

/* divider */
.divider { border:none; border-top:1px solid var(--border); margin:1.5rem 0; }

/* section label */
.section-label {
    font-family:'JetBrains Mono',monospace; font-size:0.65rem;
    letter-spacing:0.12em; text-transform:uppercase;
    color:var(--accent); margin-bottom:0.5rem;
}

/* number input overrides */
[data-testid="stNumberInput"] label { color:var(--text) !important; font-size:0.88rem !important; }
[data-testid="stNumberInput"] input {
    background:var(--surface2) !important;
    border:1px solid var(--border) !important;
    color:var(--text) !important;
    border-radius:8px !important;
    font-family:'Sora',sans-serif !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color:var(--accent) !important;
    box-shadow:0 0 0 2px var(--accent-glow) !important;
}
/* step buttons */
[data-testid="stNumberInput"] button {
    background:var(--surface2) !important;
    border-color:var(--border) !important;
    color:var(--text) !important;
}

/* hint text */
.field-hint {
    font-size:0.72rem; color:var(--muted);
    margin-top:-0.4rem; margin-bottom:0.8rem;
    font-family:'JetBrains Mono',monospace;
}

/* input label */
.input-label {
    font-size:0.88rem; font-weight:400; color:var(--text);
    margin-bottom:0.15rem; display:flex; align-items:center; gap:0.4rem;
}
.input-label i { width:1.1rem; text-align:center; color:var(--accent); }

/* selectbox */
[data-testid="stSelectbox"] label { color:var(--text) !important; font-size:0.88rem !important; }
[data-baseweb="select"] div,
[data-baseweb="select"] input {
    background:var(--surface2) !important;
    border-color:var(--border) !important;
    color:var(--text) !important;
}

/* button */
.stButton > button {
    background:linear-gradient(135deg,var(--accent) 0%,#1d4ed8 100%) !important;
    color:var(--white) !important; border:none !important;
    border-radius:8px !important; font-family:'Sora',sans-serif !important;
    font-weight:600 !important; font-size:0.9rem !important;
    padding:0.65rem 1.5rem !important; letter-spacing:0.03em !important;
    box-shadow:0 4px 24px var(--accent-glow) !important;
    transition:transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 32px rgba(37,99,235,0.4) !important;
}

/* result card */
.result-card { border-radius:12px; padding:1.5rem 1.8rem; margin-top:1.2rem; border:1px solid; }
.card-high   { background:rgba(16,185,129,0.08);  border-color:rgba(16,185,129,0.35); }
.card-medium { background:rgba(245,158,11,0.08);  border-color:rgba(245,158,11,0.35); }
.card-low    { background:rgba(239,68,68,0.08);   border-color:rgba(239,68,68,0.35);  }
.card-title  { font-size:1.4rem; font-weight:700; margin-bottom:0.4rem; }
.high-text   { color:var(--success); }
.medium-text { color:var(--warning); }
.low-text    { color:var(--danger);  }
.card-subtitle { color:var(--muted); font-size:0.82rem; margin-bottom:1.1rem; }

/* tips */
.tip-row {
    display:flex; align-items:flex-start; gap:0.6rem;
    padding:0.45rem 0; font-size:0.88rem; color:var(--text);
    border-bottom:1px solid rgba(0,0,0,0.05);
}
.tip-row:last-child { border-bottom:none; }
.tip-row i { width:1.1rem; text-align:center; margin-top:0.15rem; flex-shrink:0; color:var(--accent); }

/* metric chips */
.metric-row { display:flex; flex-wrap:wrap; gap:0.6rem; margin:1rem 0 0.5rem; }
.metric-chip {
    background:var(--surface2); border:1px solid var(--border);
    border-radius:8px; padding:0.4rem 0.75rem;
    font-size:0.78rem; color:var(--muted);
}
.metric-chip span { color:var(--text); font-weight:600; }

/* confidence bar — custom pure HTML */
.conf-wrap { margin-top:1.4rem; }
.conf-row  { display:flex; align-items:center; gap:0.8rem; margin-bottom:0.55rem; }
.conf-label { width:70px; font-size:0.8rem; color:var(--muted); flex-shrink:0; }
.conf-track { flex:1; background:var(--surface2); border-radius:999px; height:10px; overflow:hidden; }
.conf-fill  { height:100%; border-radius:999px;
              background:linear-gradient(90deg,var(--accent),#93c5fd); }
.conf-pct   { width:40px; text-align:right; font-size:0.8rem;
              font-family:'JetBrains Mono',monospace; color:var(--text); flex-shrink:0; }

/* info banner */
.info-banner {
    background:rgba(37,99,235,0.08); border:1px solid var(--border);
    border-left:3px solid var(--accent); border-radius:8px;
    padding:0.8rem 1.1rem; font-size:0.82rem; color:var(--muted);
    margin-top:1.5rem; line-height:1.6;
}

[data-testid="stMarkdownContainer"] { color:var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    try:
        with open("productivity_model.pkl", "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, KeyError):
        return None

artifacts = load_artifacts()
if artifacts is None:
    st.error("**Model not found.** Run the notebook first to generate `productivity_model.pkl`.")
    st.stop()

model                = artifacts["model"]
productivity_encoder = artifacts["productivity_encoder"]
FEATURES             = artifacts.get("features", [
    "study_hours_per_day","sleep_hours","social_media_hours","gaming_hours",
    "exercise_minutes","stress_level","assignments_completed",
    "attendance_percentage","gender_enc",
])

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Random Forest · ML Classifier</div>
    <h1>Student <span>Productivity</span><br>Analyzer</h1>
    <p>Fill in your daily habits below — the model will predict your expected productivity level.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">01 — Daily Habits</div>', unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-label"><i class="fas fa-book"></i> Study Hours / Day</div>', unsafe_allow_html=True)
    study_hours = st.number_input(
        " ", min_value=0.0, max_value=10.0,
        value=5.0, step=0.5, format="%.1f", label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">Max 10 h · typical: 3–7 h</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label"><i class="fas fa-moon"></i> Sleep Hours / Night</div>', unsafe_allow_html=True)
    sleep_hours = st.number_input(
        " ", min_value=3.0, max_value=12.0,
        value=7.0, step=0.5, format="%.1f", label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">Max 12 h · recommended: 7–9 h</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label"><i class="fas fa-mobile-alt"></i> Social Media Hours / Day</div>', unsafe_allow_html=True)
    social_media = st.number_input(
        " ", min_value=0.0, max_value=10.0,
        value=2.0, step=0.5, format="%.1f", label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">Max 10 h · healthy limit: ≤ 2 h</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label"><i class="fas fa-gamepad"></i> Gaming Hours / Day</div>', unsafe_allow_html=True)
    gaming_hours = st.number_input(
        " ", min_value=0.0, max_value=10.0,
        value=1.0, step=0.5, format="%.1f", label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">Max 10 h</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-label"><i class="fas fa-running"></i> Exercise (minutes / day)</div>', unsafe_allow_html=True)
    exercise_mins = st.number_input(
        " ", min_value=0, max_value=120,
        value=30, step=5, label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">Max 120 min · recommended: ≥ 30 min</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label"><i class="fas fa-heartbeat"></i> Stress Level</div>', unsafe_allow_html=True)
    stress_level = st.number_input(
        " ", min_value=1, max_value=10,
        value=5, step=1, label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">1 = very low · 10 = very high</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label"><i class="fas fa-check-circle"></i> Assignments Completed (this week)</div>', unsafe_allow_html=True)
    assignments = st.number_input(
        " ", min_value=0, max_value=15,
        value=7, step=1, label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">Max 15</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label"><i class="fas fa-graduation-cap"></i> Attendance Percentage</div>', unsafe_allow_html=True)
    attendance = st.number_input(
        " ", min_value=0.0, max_value=100.0,
        value=80.0, step=1.0, format="%.0f", label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">0 – 100 % · aim for ≥ 75 %</div>', unsafe_allow_html=True)

st.markdown('<div class="input-label"><i class="fas fa-venus-mars"></i> Gender</div>', unsafe_allow_html=True)
gender = st.selectbox(" ", ["Male", "Female"], label_visibility="collapsed")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("Analyze My Productivity →", type="primary", use_container_width=True):

    gender_enc = 1 if gender == "Male" else 0

    sample = pd.DataFrame([{
        "study_hours_per_day":   study_hours,
        "sleep_hours":           sleep_hours,
        "social_media_hours":    social_media,
        "gaming_hours":          gaming_hours,
        "exercise_minutes":      exercise_mins,
        "stress_level":          stress_level,
        "assignments_completed": assignments,
        "attendance_percentage": attendance,
        "gender_enc":            gender_enc,
    }])[FEATURES]

    numeric_pred = model.predict(sample)
    label        = productivity_encoder.inverse_transform(numeric_pred)[0]

    # Probabilities
    try:
        proba     = model.predict_proba(sample)[0]
        classes   = productivity_encoder.classes_
        proba_map = dict(zip(classes, proba))
        confidence = round(max(proba) * 100, 1)
    except Exception:
        proba_map  = {}
        confidence = None

    # Card config
    check = '<i class="fas fa-circle" style="color:var(--success);font-size:0.5rem;vertical-align:middle;"></i>'
    warning_circle = '<i class="fas fa-circle" style="color:var(--warning);font-size:0.5rem;vertical-align:middle;"></i>'
    danger_circle = '<i class="fas fa-circle" style="color:var(--danger);font-size:0.5rem;vertical-align:middle;"></i>'

    if label == "High":
        card_cls, txt_cls, icon, headline = "card-high", "high-text", check, "High Productivity"
        tips = [
            '<i class="fas fa-check-circle" style="color:var(--success)"></i> Your routine is well-balanced — protect it.',
            '<i class="fas fa-check-circle" style="color:var(--success)"></i> Keep exercise a non-negotiable daily habit.',
            '<i class="fas fa-check-circle" style="color:var(--success)"></i> Guard study blocks from social-media creep.',
            '<i class="fas fa-check-circle" style="color:var(--success)"></i> Maintain strong attendance; consistency compounds.',
        ]
    elif label == "Medium":
        card_cls, txt_cls, icon, headline = "card-medium", "medium-text", warning_circle, "Medium Productivity"
        tips = [
            '<i class="fas fa-chart-line"></i> Add 30–60 min of focused deep-work daily.',
            '<i class="fas fa-bed"></i> Aim for at least 7 h of sleep; below that, cognitive output drops.',
            '<i class="fas fa-clock"></i> Cap social media to under 2 h with app timers.',
            '<i class="fas fa-calendar-alt"></i> Plan next week\'s assignments every Sunday.',
        ]
    else:
        card_cls, txt_cls, icon, headline = "card-low", "low-text", danger_circle, "Low Productivity"
        tips = [
            '<i class="fas fa-bed"></i> Sleep is your highest-ROI habit — fix it first.',
            '<i class="fas fa-stop-circle"></i> Cut social media and gaming by at least 50 % immediately.',
            '<i class="fas fa-calendar-alt"></i> Build a fixed study schedule with 25-min Pomodoro blocks.',
            '<i class="fas fa-running"></i> Even 20 min of walking daily improves focus noticeably.',
            '<i class="fas fa-clipboard-list"></i> Catch up on missing assignments before new ones pile up.',
        ]

    metrics_html = f"""
    <div class="metric-row">
        <div class="metric-chip">Study <span>{study_hours}h</span></div>
        <div class="metric-chip">Sleep <span>{sleep_hours}h</span></div>
        <div class="metric-chip">Social <span>{social_media}h</span></div>
        <div class="metric-chip">Gaming <span>{gaming_hours}h</span></div>
        <div class="metric-chip">Exercise <span>{exercise_mins}min</span></div>
        <div class="metric-chip">Stress <span>{stress_level}/10</span></div>
        <div class="metric-chip">Assignments <span>{assignments}</span></div>
        <div class="metric-chip">Attendance <span>{int(attendance)}%</span></div>
    </div>
    """

    conf_text = (
        f"<br><small style='color:var(--muted);font-size:0.75rem;'>"
        f"Model confidence: {confidence}%</small>"
    ) if confidence else ""

    # Card header + metric chips
    st.markdown(f"""
    <div class="result-card {card_cls}">
        <div class="card-title {txt_cls}">{icon} {headline}</div>
        <div class="card-subtitle">Based on your input profile{conf_text}</div>
        {metrics_html}
    </div>
    """, unsafe_allow_html=True)

    # Tips rendered separately to avoid HTML parsing conflicts
    st.markdown('<div class="section-label" style="margin-top:1rem;">Recommendations</div>', unsafe_allow_html=True)
    for tip in tips:
        st.markdown(f'<div class="tip-row">{tip}</div>', unsafe_allow_html=True)

    # Custom HTML confidence bars (no st.bar_chart / no Streamlit chart code shown)
    if proba_map:
        order = ["Low", "Medium", "High"]
        bars_html = '<div class="conf-wrap"><div class="section-label" style="margin-bottom:0.8rem;">02 — Confidence Breakdown</div>'
        for cls in order:
            if cls in proba_map:
                pct = round(proba_map[cls] * 100, 1)
                bars_html += f"""
                <div class="conf-row">
                    <div class="conf-label">{cls}</div>
                    <div class="conf-track"><div class="conf-fill" style="width:{pct}%"></div></div>
                    <div class="conf-pct">{pct}%</div>
                </div>"""
        bars_html += "</div>"
        st.markdown(bars_html, unsafe_allow_html=True)

st.markdown("""
<div class="info-banner">
    <i class="fas fa-robot"></i> <strong>Model:</strong> Random Forest (200 trees) · 20 000 student records.<br>
    Productivity score 0–100 → <strong>Low</strong> &lt;40 · <strong>Medium</strong> 40–70 · <strong>High</strong> ≥70.
</div>
""", unsafe_allow_html=True)
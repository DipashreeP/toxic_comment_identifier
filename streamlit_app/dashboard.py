import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

# --- Page Config ---
st.set_page_config(
    page_title="Toxic Comment Identifier",
    page_icon="🛡️",
    layout="centered",
)

# --- Custom CSS for background image, fonts, and card ---
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%) !important;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    .stApp {
        background: url('https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80') no-repeat center center fixed;
        background-size: cover;
    }
    .stApp:before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(255, 255, 255, 0.92);
        z-index: 0;
        pointer-events: none;
    }
    .header-logo, .tech-illustration-text, .main-card, .stTextArea, .stButton, .stMarkdown, .stColumn {
        position: relative;
        z-index: 1;
    }
    .header-logo h2 {
        color: #222 !important;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-weight: 900;
        letter-spacing: 1px;
        font-size: 2.1em;
    }
    .main-card {
        background: rgba(255,255,255,0.85);
        border-radius: 14px;
        box-shadow: 0 2px 12px #dbeafe33;
        padding: 1.5em 1.2em 1.2em 1.2em;
        margin-top: 1.5em;
        margin-bottom: 2em;
        max-width: 600px;
    }
    .header-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.2em;
        margin-bottom: 1.2em;
    }
    .header-logo img {
        height: 60px;
        border-radius: 12px;
        box-shadow: 0 2px 12px #e0e7ff88;
    }
    .tech-illustration-text {
        text-align: center;
        font-size: 1.18em;
        color: #232946;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 1.2em;
        margin-top: 0.5em;
        text-shadow: none;
    }
    .stTextArea textarea {
        background: #f7f7fa !important;
        color: #222 !important;
        font-size: 1.12em;
        border-radius: 8px;
        border: 1px solid #d1d5db;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    .stButton button {
        background: #232946 !important;
        color: #fff !important;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.13em;
        border: none;
        padding: 0.6em 1.3em;
        margin: 0.2em 0.2em 0.2em 0;
        box-shadow: 0 2px 8px #dbeafe33;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        letter-spacing: 0.5px;
    }
    .stButton button:hover {
        background: #4f46e5 !important;
        color: #fff !important;
    }
    .result-card {
        background: #fff;
        color: #222;
        border-radius: 10px;
        box-shadow: 0 2px 8px #dbeafe33;
        padding: 1em 1em 0.7em 1em;
        margin-top: 0.7em;
        font-size: 1.13em;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-weight: 500;
    }
    .result-card.toxic {
        background: #ffeaea;
        color: #b91c1c;
        font-weight: 700;
        box-shadow: 0 2px 12px #ff3b3b22;
    }
    .result-card.nontoxic {
        background: #f0fdf4;
        color: #166534;
        font-weight: 700;
        box-shadow: 0 2px 8px #bbf7d022;
    }
    .result-card.rewritten {
        background: #e6f0ff;
        color: #1e293b;
        font-weight: 700;
    }
    .result-title {
        display: inline-block;
        padding: 0.12em 0.7em;
        border-radius: 14px;
        font-size: 0.98em;
        font-weight: 800;
        margin-bottom: 0.2em;
        margin-right: 0.4em;
        letter-spacing: 0.3px;
    }
    .result-title.toxic {
        background: #fff;
        color: #fb4d4d;
        border: 2px solid #fb4d4d;
    }
    .result-title.nontoxic {
        background: #fff;
        color: #22c55e;
        border: 2px solid #bbf7d0;
    }
    .result-title.nontoxic-zero {
        background: #f0fdf4;
        color: #15803d;
        border: 3px solid #22c55e;
        font-weight: 900;
        box-shadow: 0 2px 8px #bbf7d055;
    }
    .result-title.rewritten {
        background: #fff;
        color: #2563eb;
        border: 2px solid #2563eb;
    }
    .footer-visible {
        background: #fff;
        color: #232946;
        font-size: 1.08em;
        font-weight: 800;
        text-align: center;
        border-radius: 12px;
        margin: 1.5em auto 0 auto;
        padding: 0.7em 1.2em 0.7em 1.2em;
        box-shadow: 0 2px 8px #dbeafe33;
        max-width: 420px;
        letter-spacing: 0.2px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
st.sidebar.image(
    "https://huggingface.co/front/assets/huggingface_logo-noborder.svg", width=90
)
st.sidebar.title("Toxic Comment Identifier")
st.sidebar.markdown("""
**Features:**
- Detect toxic comments
- Rewrite to non-toxic
- Social feed UI
- Powered by HuggingFace LLMs
- MCP
- AWS
""")
st.sidebar.markdown("---")


# --- Header with logo and title ---
st.markdown(
    """
    <div class='header-logo'>
        <img src='https://cdn-icons-png.flaticon.com/512/5968/5968705.png' alt='Python logo'>
        <h2 style='color:#3b3b3b; margin:0; font-weight:700;'>My Tech Feed</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Tech Illustration as Text ---b
st.markdown(
    """
    <div class='tech-illustration-text'>Tech Illustration</div>
    """,
    unsafe_allow_html=True,
)

# --- Main Card ---

# --- User's Tech Post ---
user_post = "Just released my new open-source Python library for data visualization! Check it out on GitHub. 🚀 #Python #DataVisualizer"
post_time = datetime.now().strftime("%b %d, %I:%M %p")
st.markdown(
    f"""
    <div style='background-color:#f7f7fa;padding:1.2em 1em 0.7em 1em;border-radius:14px;margin-bottom:0.7em;box-shadow:0 2px 8px #eee;color:#232946;'>
        <div style='display:flex;align-items:center;'>
            <b style='color:#222;font-size:1.13em;font-family:Inter,sans-serif;'>You</b>
            <span style='color:#888;font-size:0.9em;margin-left:0.7em;'>{post_time}</span>
        </div>
        <div style='font-size:1.13em;margin:0.7em 0 0.5em 0;color:#222;font-family:Inter,sans-serif;'>{user_post}</div>
        <div style='display:flex;align-items:center;gap:1.2em;font-size:1.1em;color:#FF6F61;'>
            <span>❤️  24</span>
            <span>💬  1</span>
            <span>🔁  2</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Other User's Comment Input (toxic reply) ---
st.markdown("<b style='color:#555;'>Comment from <span style='color:#FF6F61;'>@dev_rant</span>:</b>", unsafe_allow_html=True)
user_comment = st.text_area("", key="comment_input", height=70, placeholder="Type a reply (try something rude or toxic for demo)...")

# Center the buttons horizontally
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        bcol1, bcol2 = st.columns(2)
        with bcol1:
            analyze_btn = st.button("🔎 Analyze Toxicity")
        with bcol2:
            rewrite_btn = st.button("✨ Rewrite Comment")
# --- Results Card ---
if analyze_btn and user_comment:
    with st.spinner("Analyzing for toxicity..."):
        resp = requests.post(f"{API_URL}/detect_toxicity", json={"text": user_comment})
        if resp.status_code == 200:
            result = resp.json()
            score = result.get("score")
            if score is None:
                st.error(result.get("error", "No score returned from backend."))
                st.stop()
            if result["toxic"]:
                st.markdown(
                    f"<div class='result-card toxic'><span class='result-title toxic'>🚨 Toxic!</span> (score: <b>{score:.2f}</b>)</div>",
                    unsafe_allow_html=True,
                )
            elif score == 0:
                st.markdown(
                    f"<div class='result-card nontoxic'><span class='result-title nontoxic-zero'>🟢 Non Toxic</span></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='result-card nontoxic'><span class='result-title nontoxic'>✅ Not toxic!</span> (score: <b>{score:.2f}</b>)</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.error("Toxicity detection failed.")
if rewrite_btn and user_comment:
    with st.spinner("Rewriting comment..."):
        rewrite_resp = requests.post(f"{API_URL}/rewrite", json={"text": user_comment})
        if rewrite_resp.status_code == 200:
            rewritten = rewrite_resp.json()["rewritten"]
            st.markdown(
                f"<div class='result-card rewritten'><span class='result-title rewritten'>Rewritten Comment:</span><br><span>{rewritten}</span></div>",
                unsafe_allow_html=True,
            )
        else:
            st.error("Rewrite failed.")
st.markdown("<div style='margin-bottom:2.2em;'></div>", unsafe_allow_html=True)

# --- End Main Card ---

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:0.9em;color:#888;'>Made with ❤️ using HuggingFace, MCP, and Streamlit</div>",
    unsafe_allow_html=True,
) 
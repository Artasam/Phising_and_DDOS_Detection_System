import os

import streamlit as st
from dotenv import load_dotenv


def _init_secrets_or_env() -> None:
    """
    Prefer Streamlit secrets (cloud), fall back to local .env.
    """
    try:
        # In Streamlit Cloud, secrets are provided via st.secrets
        groq_key = st.secrets["GROQ_API_KEY"]
        os.environ["GROQ_API_KEY"] = groq_key

        # VT_API_KEY may be optional
        vt_key = st.secrets.get("VT_API_KEY", None)
        if vt_key:
            os.environ["VT_API_KEY"] = vt_key
    except Exception:
        # Local development: load from .env file instead
        load_dotenv()


_init_secrets_or_env()

from workflows.langgraph_phishing_flow import app as phishing_app
from workflows.langgraph_ddos_flow import build_ddos_graph


st.set_page_config(
    page_title="Phishing & DDoS Detection Agent",
    page_icon="🛡️",
    layout="wide",
)


def _inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        .main {
            background: radial-gradient(circle at top left, #020617 0, #020617 35%, #020617 100%);
            color: #e5e7eb;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #020617 0%, #020617 40%, #020617 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.25);
        }
        .stMetric {
            background-color: rgba(15, 23, 42, 0.85) !important;
            border-radius: 0.5rem;
            padding: 0.5rem 0.75rem;
            border: 1px solid rgba(56, 189, 248, 0.45);
        }
        .app-card {
            background: radial-gradient(circle at top left, rgba(15,23,42,0.95) 0, rgba(15,23,42,0.9) 45%, rgba(15,23,42,0.98) 100%);
            border-radius: 1rem;
            padding: 1.25rem 1.5rem;
            border: 1px solid rgba(148, 163, 184, 0.4);
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.85);
        }
        .app-card h3, .app-card h4 {
            margin-top: 0.1rem;
            margin-bottom: 0.35rem;
        }
        .app-tag {
            display: inline-flex;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            border: 1px solid rgba(148, 163, 184, 0.5);
            color: #e5e7eb;
            background: linear-gradient(90deg, rgba(56, 189, 248, 0.18), rgba(59, 130, 246, 0.1));
        }
        .app-title {
            font-size: 2.3rem;
            font-weight: 700;
            margin-top: 0.3rem;
            margin-bottom: 0.2rem;
            background: linear-gradient(120deg, #e5e7eb, #38bdf8, #a855f7);
            -webkit-background-clip: text;
            color: transparent;
        }
        .app-subtitle {
            font-size: 0.95rem;
            color: #cbd5f5;
            max-width: 40rem;
        }
        /* Tabs */
        button[data-baseweb="tab"] {
            border-radius: 999px !important;
            padding: 0.35rem 1.2rem !important;
            border: 1px solid transparent !important;
            font-weight: 500 !important;
            color: #cbd5e1 !important;
            background: transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.32), rgba(29, 78, 216, 0.8)) !important;
            border-color: rgba(56, 189, 248, 0.7) !important;
            color: white !important;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.9);
        }
        /* Buttons */
        .stButton>button {
            border-radius: 999px;
            padding: 0.45rem 1.4rem;
            border: 1px solid rgba(56, 189, 248, 0.6);
            background: radial-gradient(circle at top left, #38bdf8 0, #2563eb 40%, #4f46e5 100%);
            color: white;
            font-weight: 600;
            box-shadow: 0 14px 28px rgba(15, 23, 42, 0.85);
        }
        .stButton>button:hover {
            border-color: rgba(248, 250, 252, 0.9);
            transform: translateY(-1px);
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.95);
        }
        /* Inputs */
        .stTextInput>div>div>input,
        .stTextArea>div>textarea {
            border-radius: 0.75rem !important;
        }
        .stNumberInput>div>div>input {
            border-radius: 0.75rem !important;
        }
        .stSelectbox>div>div {
            border-radius: 0.75rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_header():
    _inject_custom_css()

    left, right = st.columns([2.3, 1.3])
    with left:
        st.markdown('<span class="app-tag">Security · LangGraph · Groq</span>', unsafe_allow_html=True)
        st.markdown(
            '<div class="app-title">Phishing & DDoS Detection Agent</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="app-subtitle">A hybrid SOC-style assistant that combines rule-based signals, '
            'VirusTotal, and Groq LLM reasoning to triage phishing emails and DDoS traffic.</p>',
            unsafe_allow_html=True,
        )
    with right:
        groq_ok = bool(os.getenv("GROQ_API_KEY"))
        vt_ok = bool(os.getenv("VT_API_KEY"))
        st.metric("GROQ API", "Configured" if groq_ok else "Missing", delta=None)
        st.metric("VirusTotal", "Configured" if vt_ok else "Optional", delta=None)
        st.caption(
            "Secrets are loaded from `st.secrets` in the cloud, or `.env` when running locally."
        )

    st.markdown("---")


def phishing_tab():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("### ✉️ Phishing Detection")
    st.markdown(
        "Provide email details and let the agent decide if it is **phishing**."
    )

    with st.form("phishing_form"):
        url = st.text_input(
            "URL in the email",
            placeholder="https://example.com/login",
        )
        attachment = st.text_input(
            "Attachment filename (if any)",
            placeholder="invoice.pdf",
        )
        email_text = st.text_area(
            "Email body text",
            placeholder="Dear user, your account has been suspended. Please verify urgently...",
            height=160,
        )

        submitted = st.form_submit_button("Analyze Email 🔍")

    if submitted:
        log_input = {
            "url": url,
            "attachment": attachment,
            "email_text": email_text,
        }

        with st.spinner("Running phishing detection workflow..."):
            try:
                response = phishing_app.invoke({"log": log_input})
            except Exception as e:
                st.error(f"Error while running phishing workflow: {e}")
                return

        decision = response.get("decision", "No decision returned.")
        results = response.get("results", {})

        st.success("Analysis complete.")

        cols = st.columns([2, 1])
        with cols[0]:
            st.markdown("#### 🧠 LLM Decision")
            st.write(decision)

        with cols[1]:
            st.markdown("#### 🧪 Indicator Summary")
            st.json(results)

    st.markdown("</div>", unsafe_allow_html=True)


def ddos_tab():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("### 🌐 DDoS Detection")
    st.markdown(
        "Fill in traffic log details to detect potential **DDoS attacks**."
    )

    col1, col2 = st.columns(2)
    with col1:
        src_ip = st.text_input("Source IP", "192.168.1.100")
        dst_ip = st.text_input("Destination IP", "10.0.0.10")
        timestamp = st.text_input(
            "Timestamp (ISO 8601)",
            "2025-07-16T10:00:00Z",
        )
        request_type = st.selectbox("Request Type", ["GET", "POST", "PUT", "DELETE"])

    with col2:
        path = st.text_input("Path / Endpoint", "/index.html")
        packet_size = st.number_input(
            "Packet size (bytes)",
            min_value=0,
            value=800,
            step=50,
        )
        rate_per_minute = st.number_input(
            "Request rate (per minute)",
            min_value=0,
            value=50,
            step=10,
        )
        user_agent = st.text_input(
            "User-Agent",
            "Mozilla/5.0",
        )

    if st.button("Analyze Traffic 🔍"):
        log = {
            "timestamp": timestamp,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "request_type": request_type,
            "path": path,
            "packet_size": packet_size,
            "rate_per_minute": rate_per_minute,
            "user_agent": user_agent,
        }

        with st.spinner("Running DDoS detection workflow..."):
            try:
                graph = build_ddos_graph()
                state = {"log": log}
                result_state = graph.invoke(state)
            except Exception as e:
                st.error(f"Error while running DDoS workflow: {e}")
                return

        result = result_state.get("result", {})
        is_ddos = result.get("is_ddos", False)
        rule_reason = result.get("rule_reason", "")
        llm_reason = result.get("llm_reason", "")

        if is_ddos:
            st.error("🚨 DDoS attack detected")
        else:
            st.success("✅ Traffic appears normal")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 📏 Rule-Based Analysis")
            st.write(rule_reason or "No rule-based indicators triggered.")
        with col_b:
            st.markdown("#### 🧠 LLM Explanation")
            st.write(llm_reason or "No LLM explanation available.")

        with st.expander("Full log input"):
            st.json(log)

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    show_header()
    tabs = st.tabs(["✉️ Phishing", "🌐 DDoS"])

    with tabs[0]:
        phishing_tab()
    with tabs[1]:
        ddos_tab()


if __name__ == "__main__":
    main()


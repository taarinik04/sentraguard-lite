import streamlit as st
import requests


API_URL = "http://sentraguard-api:8000/analyze"

st.set_page_config(
    page_title="SentraGuard Lite",
    page_icon="🛡️",
    layout="wide"
)



st.markdown("""
<style>

/* Page Title */
h1 {
    font-size: 3.4rem !important;
    font-weight: 700 !important;
}

/* Subtitle */
[data-testid="stCaptionContainer"] {
    font-size: 1.2rem !important;
}

/* Prompt & Context labels */
[data-testid="stWidgetLabel"] p {
    font-size: 1.3rem !important;
    font-weight: 600 !important;
}

/* Text inside text areas */
.stTextArea textarea {
    font-size: 1.15rem !important;
}

/* Analyze button */
div[data-testid="stButton"] button p {
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* Risk Score / Risk Tags / Sanitized Prompt headings */
h2 {
    font-size: 1.8rem !important;
    font-weight: 600 !important;
}

/* Metric titles */
[data-testid="stMetricLabel"] p {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    font-size: 2.8rem !important;
    font-weight: 700 !important;
}

/* Success / Warning / Error boxes */
[data-testid="stAlertContainer"] {
    font-size: 1.1rem !important;
}

/* Expander title */
.streamlit-expanderHeader {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)



st.markdown(
    "<h1>🛡️ SentraGuard Lite</h1>",
    unsafe_allow_html=True
)

st.caption(
    "GenAI Security Gateway for Prompt Injection, PII Detection and RAG Security Analysis"
)

st.divider()



col1, col2 = st.columns(2)

with col1:
    prompt = st.text_area(
        "Prompt",
        height=250,
        placeholder="Enter user prompt here..."
    )

with col2:
    context = st.text_area(
        "Context Document",
        height=250,
        placeholder="Paste retrieved context here..."
    )

analyze_button = st.button(
    "🛡️ Analyze Prompt",
    use_container_width=True
)



if analyze_button:

    payload = {
        "prompt": prompt,
        "context_docs": [
            {
                "id": "doc-1",
                "text": context
            }
        ] if context else [],
        "metadata": {
            "app_id": "streamlit",
            "user_id": "demo-user",
            "request_id": "demo-request"
        }
    }

    try:

        response = requests.post(
            API_URL,
            json=payload
        )

        result = response.json()

        st.divider()

        decision = result["decision"]
        score = result["risk_score"]

        if decision == "allow":
            st.success("✅ Decision: ALLOW")

        elif decision == "transform":
            st.warning("⚠️ Decision: TRANSFORM")

        else:
            st.error("🚫 Decision: BLOCK")

        metric1, metric2 = st.columns(2)

        with metric1:
            st.metric(
                "Risk Score",
                score
            )

        with metric2:
            st.metric(
                "Risk Tags",
                len(result["risk_tags"])
            )

        st.markdown("## Risk Score")

        st.progress(
            min(score / 100, 1.0)
        )

        st.markdown("## Risk Tags")

        if result["risk_tags"]:
            for tag in result["risk_tags"]:
                st.info(tag)

        else:
            st.success("No risk tags detected")

        st.markdown("## Sanitized Prompt")

        st.code(
            result["sanitized_prompt"],
            language="text"
        )

        with st.expander("View Raw JSON Response"):
            st.json(result)

    except Exception as e:

        st.error(
            f"Error connecting to API: {str(e)}"
        )
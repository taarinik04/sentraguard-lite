import os
import streamlit as st
import requests


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/analyze"
)

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


# Sidebar Metadata
st.sidebar.header("Request Metadata")

app_id = st.sidebar.text_input(
    "App ID",
    value="sentraguard-ui"
)

user_id = st.sidebar.text_input(
    "User ID",
    value="user-001"
)

request_id = st.sidebar.text_input(
    "Request ID",
    value="req-001"
)


col1, col2 = st.columns(2)

with col1:
    prompt = st.text_area(
        "Prompt",
        height=250,
        placeholder="Enter user prompt here..."
    )

with col2:

    context1 = st.text_area(
        "Context Document 1",
        height=120,
        placeholder="Paste context document 1..."
    )

    context2 = st.text_area(
        "Context Document 2",
        height=120,
        placeholder="Paste context document 2..."
    )

    context3 = st.text_area(
        "Context Document 3",
        height=120,
        placeholder="Paste context document 3..."
    )


analyze_button = st.button(
    "🛡️ Analyze Prompt",
    use_container_width=True
)


if analyze_button:

    context_docs = []

    if context1.strip():
        context_docs.append(
            {
                "id": "doc-1",
                "text": context1
            }
        )

    if context2.strip():
        context_docs.append(
            {
                "id": "doc-2",
                "text": context2
            }
        )

    if context3.strip():
        context_docs.append(
            {
                "id": "doc-3",
                "text": context3
            }
        )

    payload = {
        "prompt": prompt,
        "context_docs": context_docs,
        "metadata": {
            "app_id": app_id,
            "user_id": user_id,
            "request_id": request_id
        }
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        st.divider()

        decision = result["decision"]
        score = result["risk_score"]

        if decision == "allow":
            st.success("Decision: ALLOW")

        elif decision == "transform":
            st.warning("Decision: TRANSFORM")

        else:
            st.error("Decision: BLOCK")

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
import streamlit as st
from streamlit.components.v1 import html

from scripts.query_engine import (
    analyze_incident,
    add_incident_to_knowledgebase
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="ResolveOrange",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# ADAPTIVE CSS (STREAMLIT LIGHT/DARK)
# -----------------------------------

st.markdown("""
<style>

/* -----------------------------------
THEME VARIABLES
----------------------------------- */

:root {
    --resolve-color: #003B70;
}

/* Dark Theme */

@media (prefers-color-scheme: dark) {

    :root {
        --resolve-color: #4DA3FF;
    }

}

/* -----------------------------------
MAIN APP
----------------------------------- */

.stApp {
    font-family: "Segoe UI", sans-serif;
}

/* -----------------------------------
SIDEBAR
----------------------------------- */

section[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.15);
}

/* -----------------------------------
TEXT AREA
----------------------------------- */

textarea {
    border-radius: 14px !important;
    padding: 14px !important;
    font-size: 15px !important;
}

/* -----------------------------------
BUTTONS
----------------------------------- */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
    font-weight: 600;
    background-color: #FF6200;
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    opacity: 0.9;
}

/* -----------------------------------
MAIN HEADER
----------------------------------- */

.main-header {
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 0;
}

/* -----------------------------------
SUB HEADER
----------------------------------- */

.sub-header {
    color: inherit;
    opacity: 0.75;
    margin-top: 6px;
    margin-bottom: 30px;
    font-size: 16px;
}

/* -----------------------------------
WORKSPACE CARD
----------------------------------- */

.workspace-card {
    padding: 0px;
    border: none;
    background: transparent;
}

/* -----------------------------------
RCA OUTPUT
----------------------------------- */

.rca-box {
    padding: 24px;
    border-radius: 18px;
    border-left: 5px solid #FF6200;
    border-top: 1px solid rgba(128,128,128,0.15);
    border-right: 1px solid rgba(128,128,128,0.15);
    border-bottom: 1px solid rgba(128,128,128,0.15);
    line-height: 1.8;
    font-size: 15px;
    margin-top: 10px;
}

/* -----------------------------------
SECTION TITLE
----------------------------------- */

.section-title {
    font-weight: 600;
    font-size: 18px;
    margin-bottom: 10px;
}

/* -----------------------------------
FOOTER
----------------------------------- */

.footer-text {
    text-align: center;
    opacity: 0.7;
    margin-top: 40px;
    font-size: 13px;
}

/* -----------------------------------
STATUS CARDS
----------------------------------- */

.status-card {
    padding: 12px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.12);
    background-color: rgba(255,255,255,0.02);
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; margin-bottom: 18px;'>
            <div style='font-size:52px; line-height:1; margin-bottom:8px;'>🦁</div>
            <div style='font-size:28px; font-weight:700; margin-bottom:4px;'>
                <span style='color:var(--resolve-color);'>Resolve</span><span style='color:#FF6200;'>Orange</span>
            </div>
            <div style='font-size:13px; margin-top:5px; opacity:0.75; color:#5B6575;'>
                Enterprise Operational Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Workspace")

    st.markdown("""
- Incident RCA
- Historical Correlation
- Operational Intelligence
- Enterprise Incident Memory
- RCA Knowledge Retrieval
""")

    st.divider()

    st.markdown("### Supported Operations")

    st.markdown("""
- Deployment Failures
- Scheduler Issues
- ETL Disruptions
- Dashboard Failures
- Reporting Incidents
- Production Alerts
""")

    st.divider()

    st.markdown("### AI Stack")

    st.markdown("""
- Groq LLM
- FAISS Retrieval
- Sentence Transformers
- Streamlit
""")

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("""
<div class="main-header">

<span style="color:var(--resolve-color);">
    Resolve
</span><span style="color:#FF6200;">
    Orange
</span>

</div>

<div class="sub-header">
Enterprise Operational Intelligence & RCA Workspace
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# OPERATIONAL STATUS BAR
# -----------------------------------

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.markdown("""
    <div class="status-card">
        <div style="opacity:0.7; font-size:13px; margin-bottom:4px;">
            System Status
        </div>
        <div style="font-weight:600; font-size:16px;">
            🟢 Operational
        </div>
    </div>
    """, unsafe_allow_html=True)

with status_col2:
    st.markdown("""
    <div class="status-card">
        <div style="opacity:0.7; font-size:13px; margin-bottom:4px;">
            Knowledge Base
        </div>
        <div style="font-weight:600; font-size:16px;">
            🟢 Connected
        </div>
    </div>
    """, unsafe_allow_html=True)

with status_col3:
    st.markdown("""
    <div class="status-card">
        <div style="opacity:0.7; font-size:13px; margin-bottom:4px;">
            AI Engine
        </div>
        <div style="font-weight:600; font-size:16px;">
            🟢 Active
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------
# INPUT SECTION
# -----------------------------------

st.markdown("""
<div class="section-title">
Enterprise Incident Input
</div>
""", unsafe_allow_html=True)

user_input = st.text_area(
    label="",
    height=180,
    key="incident_input",
    placeholder="""
Example:

Scheduler service stopped unexpectedly after deployment.
Dashboard refresh jobs failed across production.
ETL queue stuck for 45 minutes.
Users unable to access refreshed reports.

(Press Enter to Analyze • Shift+Enter for new line)
"""
)

# -----------------------------------
# ENTER KEY SUBMISSION
# -----------------------------------

enter_pressed = html(
    """
    <script>

    const doc = window.parent.document;

    const textarea = doc.querySelector('textarea');

    textarea.addEventListener('keydown', function(event) {

        if (event.key === 'Enter' && !event.shiftKey) {

            event.preventDefault();

            const buttons = doc.querySelectorAll('button');

            buttons.forEach(btn => {

                if (btn.innerText.includes('Analyze Incident')) {
                    btn.click();
                }

            });

        }

    });

    </script>
    """,
    height=0
)

analyze_clicked = st.button(
    "Analyze Incident",
    use_container_width=True
)

# -----------------------------------
# INCIDENT ANALYSIS
# -----------------------------------

if analyze_clicked:

    if not user_input.strip():

        st.warning(
            "Please enter enterprise incident details."
        )

    else:

        with st.spinner(
            "Analyzing enterprise operational incident..."
        ):

            try:

                # -----------------------------------
                # ANALYZE INCIDENT
                # -----------------------------------

                retrieved_context = []

                result = analyze_incident(
                    user_input,
                    return_context=True
                )

                response = result["response"]

                retrieved_context = result.get(
                    "context",
                    []
                )

                # -----------------------------------
                # SCOPE RESTRICTION CHECK
                # -----------------------------------

                if "Scope Restriction Notice" in response:

                    st.warning(
                        "Query outside enterprise operational scope."
                    )

                    st.markdown(response)

                    st.stop()

                # -----------------------------------
                # DETECT SEVERITY
                # -----------------------------------

                severity = "Medium"

                if "Critical" in response:
                    severity = "Critical"

                elif "High" in response:
                    severity = "High"

                elif "Low" in response:
                    severity = "Low"

                # -----------------------------------
                # STORE INCIDENT
                # -----------------------------------

                incident_id = add_incident_to_knowledgebase(
                    user_input,
                    response
                )

                # -----------------------------------
                # HEADER
                # -----------------------------------

                st.markdown("## Incident Analysis")

                st.caption(
                    f"Incident ID: {incident_id}"
                )

                # -----------------------------------
                # SEVERITY
                # -----------------------------------

                if severity == "Critical":

                    st.error(
                        f"Severity Level: {severity}"
                    )

                elif severity == "High":

                    st.warning(
                        f"Severity Level: {severity}"
                    )

                elif severity == "Medium":

                    st.info(
                        f"Severity Level: {severity}"
                    )

                else:

                    st.success(
                        f"Severity Level: {severity}"
                    )

                # -----------------------------------
                # RCA OUTPUT
                # -----------------------------------

                st.markdown(
                    f"""
<div class="rca-box">

{response}

</div>
""",
                    unsafe_allow_html=True
                )

                # -----------------------------------
                # ENTERPRISE CONTEXT VIEWER
                # -----------------------------------

                with st.expander(
                    "Retrieved Enterprise Context"
                ):

                    st.caption(
                        "Semantic operational knowledge retrieved from enterprise vector database"
                    )

                    if retrieved_context:

                        for i, chunk in enumerate(retrieved_context):

                            st.markdown(
                                f"### Context Chunk {i + 1}"
                            )

                            cleaned_chunk = chunk.replace(
                                "**",
                                ""
                            )

                            cleaned_chunk = cleaned_chunk.replace(
                                "severity: Low",
                                "severity: LOW"
                            )

                            cleaned_chunk = cleaned_chunk.replace(
                                "severity: Medium",
                                "severity: MEDIUM"
                            )

                            cleaned_chunk = cleaned_chunk.replace(
                                "severity: High",
                                "severity: HIGH"
                            )

                            cleaned_chunk = cleaned_chunk.replace(
                                "severity: Critical",
                                "severity: CRITICAL"
                            )

                            st.code(
                                cleaned_chunk[:2500],
                                language="yaml"
                            )

                    else:

                        st.info(
                            "No enterprise context retrieved."
                        )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("""
<div class="footer-text">
AI-Powered Enterprise Operational Intelligence Platform
</div>
""", unsafe_allow_html=True)

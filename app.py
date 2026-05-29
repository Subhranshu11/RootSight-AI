import streamlit as st

from scripts.query_engine import (
    analyze_incident,
    add_incident_to_knowledgebase
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="ReportOps AI Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
    border-right: 1px solid #30363D;
}

/* Input Box */
textarea {
    border-radius: 12px !important;
    border: 1px solid #30363D !important;
    background-color: #161B22 !important;
    color: white !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3rem;
    font-weight: 600;
    background-color: #2383E2;
    color: white;
    border: none;
}

.stButton > button:hover {
    background-color: #1A6FC2;
}

/* Chat Style Containers */
.chat-container {
    background-color: #161B22;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #30363D;
    margin-top: 15px;
}

/* RCA Output */
.rca-box {
    background-color: #0D1117;
    padding: 24px;
    border-radius: 14px;
    border: 1px solid #30363D;
    line-height: 1.8;
    font-size: 15px;
}

/* Header */
.main-header {
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 0;
}

.sub-header {
    color: #8B949E;
    margin-top: 0;
    margin-bottom: 25px;
}

/* Footer */
.footer-text {
    color: #8B949E;
    text-align: center;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.markdown("## 🤖 ReportOps AI")

    st.caption(
        "Enterprise Operational Intelligence Workspace"
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
ReportOps Copilot
</div>

<div class="sub-header">
Enterprise Operational Intelligence & RCA Workspace
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# CHAT-LIKE INCIDENT INPUT
# -----------------------------------

st.markdown("""
<div class="chat-container">
""", unsafe_allow_html=True)

user_input = st.text_area(
    "Enter Enterprise Incident",
    height=180,
    placeholder="""
Example:

Scheduler service stopped unexpectedly after deployment.
Dashboard refresh jobs failed across production.
ETL queue stuck for 45 minutes.
Users unable to access refreshed reports.
"""
)

analyze_clicked = st.button(
    "Analyze Incident"
)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------
# ANALYSIS SECTION
# -----------------------------------

if analyze_clicked:

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not user_input.strip():

        st.warning(
            "Please enter incident details."
        )

    else:

        with st.spinner(
            "Analyzing enterprise operational incident..."
        ):

            try:

                # -----------------------------------
                # ANALYZE INCIDENT
                # -----------------------------------

                response = analyze_incident(
                    user_input
                )

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
                # INCIDENT HEADER
                # -----------------------------------

                st.markdown("## Incident Analysis")

                # -----------------------------------
                # INCIDENT ID
                # -----------------------------------

                st.caption(
                    f"Incident ID: {incident_id}"
                )

                # -----------------------------------
                # SEVERITY DISPLAY
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
                # METRICS
                # -----------------------------------

                st.divider()

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Operational Mode",
                    "Enterprise RCA"
                )

                col2.metric(
                    "Knowledge Retrieval",
                    "FAISS Semantic Search"
                )

                col3.metric(
                    "LLM Engine",
                    "llama-3.3-70b-versatile"
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

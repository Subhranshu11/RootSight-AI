import streamlit as st

from scripts.query_engine import (
    analyze_incident,
    add_incident_to_knowledgebase
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Ops RCA Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("🤖 AI Ops RCA Assistant")

st.markdown("""
Enterprise Operational Intelligence Copilot

Analyze:
- Deployment failures
- ETL issues
- Scheduler disruptions
- Incident tickets
- Operational RCA
""")

# -----------------------------------
# USER INPUT
# -----------------------------------

user_input = st.text_area(
    "Paste Incident Log / Incident Description",
    height=250,
    placeholder="""
Example:

Scheduler service stopped unexpectedly after deployment.
Downstream dashboard refresh jobs failed.
ETL queue stuck for 45 minutes.
Users unable to access refreshed reports.
"""
)

# -----------------------------------
# ANALYZE BUTTON
# -----------------------------------

if st.button("Analyze Incident"):

    # Validation
    if not user_input.strip():

        st.warning("Please enter incident details.")

    else:

        # Loading spinner
        with st.spinner("Analyzing incident and retrieving enterprise knowledge..."):

            try:

                # -----------------------------------
                # ANALYZE INCIDENT
                # -----------------------------------

                response = analyze_incident(user_input)

                # -----------------------------------
                # DISPLAY RESPONSE
                # -----------------------------------

                st.subheader("📌 AI RCA Analysis")

                st.write(response)

                # -----------------------------------
                # SAVE INCIDENT INTO KNOWLEDGE BASE
                # -----------------------------------

                incident_id = add_incident_to_knowledgebase(
                    user_input,
                    response
                )

                # -----------------------------------
                # SUCCESS MESSAGE
                # -----------------------------------

                st.success(
                    f"Incident analyzed and stored successfully. Incident ID: {incident_id}"
                )

            except Exception as e:

                st.error(f"Error: {str(e)}")

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "AI-Powered Operational RCA & Enterprise Incident Intelligence System"
)

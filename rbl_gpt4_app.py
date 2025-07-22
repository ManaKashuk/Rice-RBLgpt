import streamlit as st

# Sidebar for workflow selection
workflow = st.sidebar.selectbox("Select Workflow", ["Pre-Award", "Post-Award"])

# Title and description
st.title("RBLgpt Assistant")
st.markdown("Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad")

# Simulated responses categorized by workflow
pre_award_responses = {
    "What research administration training is offered by ORA?":
        "ORA offers self-paced and instructor-led training programs for research administrators.",
    "How many professional development hours are needed for ORA?":
        "Emory requires a specific number of professional development hours per year. Refer to the policy for details.",
    "Where can I find the professional development tracking log?":
        "You can find the tracking log on the ORA website under the Training section.",
    "What are the training requirements for staff involved in NIH clinical trials at Emory?":
        "Staff must complete NIH-required certifications and maintain compliance through continuing education.",
    "What system will help me determine the status of the CT agreement?":
        "Use the Clinical Trial Management System (CTM) to track agreement status.",
    "How can I access the FORT, and what features does it offer for clinical trial financial management?":
        "FORT provides budget projections, expense tracking, and financial reporting tools.",
    "Tell me about Research Training and provide details on the continuing education policy requirements.":
        "Research training includes Emory’s continuing education policy and guidance on meeting requirements.",
    "What is Research.gov?":
        "Research.gov is a federal portal for research administration, proposal submission, and award tracking.",
    "What is the Davis-Bacon Act?":
        "The Davis-Bacon Act governs wage requirements for federally funded construction projects."
}

post_award_responses = {
    "What is the award start date for \"Meissa RSV Vaccine MV-006\"?":
        "The award start date is listed in the FORT database under the award details.",
    "What is the Award PI ID for \"Meissa RSV Vaccine MV-006\"?":
        "The Principal Investigator ID is available in Emory’s research administration records.",
    "In the Sample FORT file, tell me about the award Emory-CHOA Clinical Immunization.":
        "This award includes funding amounts, key milestones, and reporting requirements.",
    "What is the Award Closeout process?":
        "The closeout process includes final reporting, documentation, and financial reconciliation.",
    "How will eNOAs be distributed?":
        "Electronic Notices of Award (eNOAs) are distributed by the central ORA team via email.",
    "What is the escalation process if I am unable to validate and/or resolve a financial compliance or reporting issue?":
        "Contact your department administrator, then escalate to ORA compliance team if unresolved."
}

# Input box for user question
user_question = st.text_input("Ask a question related to your selected workflow:")

# Display response based on workflow and question
if user_question:
    if workflow == "Pre-Award":
        response = pre_award_responses.get(user_question,
                    f"Simulated Pre-Award response: No match found in database for '{user_question}'")
    else:
        response = post_award_responses.get(user_question,
                    f"Simulated Post-Award response: No match found in database for '{user_question}'")
    st.markdown(f"**Response:** {response}")

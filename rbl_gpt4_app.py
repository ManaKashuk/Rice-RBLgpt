import streamlit as st
from PIL import Image

logo_path = "UploadedImage3.jpg"
logo = Image.open(logo_path)

st.set_page_config(page_title="RBL GPT Assistant", page_icon="🧬", layout="wide")

st.image(logo, width=150)
st.title("RBLgpt Assistant")
st.subheader("Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad")
st.markdown("Welcome, **Mana Kashuk**! 👋")

workflow = st.sidebar.radio("Select Workflow", ["Pre-Award", "Post-Award"])

user_question = st.text_input("Ask a question related to research administration:")

responses = {
    "Pre-Award": {
        "What research administration training is offered by ORA?": "ORA offers self-paced and instructor-led courses for research administrators.",
        "How many professional development hours are needed for ORA?": "Emory requires a specific number of professional development hours per year. Refer to the policy for details.",
        "Where can I find the professional development tracking log?": "The tracking log is available on the ORA website under the Training section.",
        "What are the training requirements for staff involved in NIH clinical trials at Emory?": "Staff must complete NIH-required certifications and maintain compliance through continuing education.",
        "What system will help me determine the status of the CT agreement?": "Use the Clinical Trial Management System (CTM) to track agreement status.",
        "How can I access the FORT, and what features does it offer for clinical trial financial management?": "FORT provides budget projections, expense tracking, and financial reporting tools.",
        "What is Research.gov?": "Research.gov is a federal portal for research administration and grant management.",
        "What is the Davis-Bacon Act?": "The Davis-Bacon Act governs wage requirements for federally funded construction projects."
    },
    "Post-Award": {
        "What is the Award Closeout process?": "The closeout process includes final reporting, documentation, and compliance checks.",
        "Tell me about Research Training and provide details on the continuing education policy requirements.": "Research training includes continuing education programs and policy guidance for compliance.",
        "How will eNOAs be distributed?": "Electronic Notices of Award (eNOAs) are distributed by the central ORA team via email.",
        "What is the escalation process if I am unable to validate and/or resolve a financial compliance or reporting issue?": "Contact your department administrator, then escalate to ORA leadership if unresolved.",
        "What is the award start date for \"Meissa RSV Vaccine MV-006\"?": "The award start date is listed in the FORT database under the award details.",
        "What is the Award PI ID for \"Meissa RSV Vaccine MV-006\"?": "The PI ID is available in Emory’s research administration records.",
        "In the Sample FORT file, tell me about the award Emory-CHOA Clinical Immunization.": "The award includes funding amounts, milestones, and reporting requirements."
    }
}

if user_question:
    answer = responses.get(workflow, {}).get(user_question)
    if answer:
        st.success(f"Simulated {workflow} response:\n\n{answer}")
    else:
        st.warning(f"Simulated {workflow} response: No match found in database.")

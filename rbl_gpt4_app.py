# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 13:38:21 2025

@author: ManaK
"""

import streamlit as st

response_map = {
    "what research administration training is offered by ora": 
        "ORAgpt provides a detailed list of training programs, including self-paced and instructor-led courses. Continuing education is emphasized.",
    "how many professional development hours are needed for ora": 
        "ORAgpt outlines the required hours per Emory’s policy and provides links to additional resources.",
    "where can i find the professional development tracking log": 
        "The tracking log is available on the ORA website. ORAgpt specifies its location and how to access it.",
    "what are the training requirements for staff involved in nih clinical trials at emory": 
        "NIH training requirements include certifications and compliance steps. ORAgpt provides a comprehensive explanation.",
    "what system will help me determine the status of the ct agreement": 
        "ORAgpt lists systems like CTM and describes features for agreement status tracking.",
    "how can i access the fort, and what features does it offer for clinical trial financial management": 
        "ORAgpt explains the FORT access process and describes features like budget projections and expense tracking.",
    "what is the award closeout process": 
        "ORAgpt outlines the award closeout steps, timelines, documentation, and responsibilities.",
    "tell me about research training and provide details on the continuing education policy requirements": 
        "ORAgpt provides an overview of research training and guidance on meeting continuing education policies.",
    "how will enoas be distributed": 
        "ORAgpt specifies the eNOA distribution method and responsible departments.",
    "what is the escalation process if i am unable to validate and/or resolve a financial compliance or reporting issue": 
        "ORAgpt provides a step-by-step escalation process and contact points.",
    "what is research.gov": 
        "ORAgpt explains Research.gov and its relevance to research administrators.",
    "what is the davis-bacon act": 
        "ORAgpt summarizes the Davis-Bacon Act and its implications for federally funded construction projects.",
    "what is the award start date for \"meissa rsv vaccine mv-006\"": 
        "ORAgpt retrieves and presents the award start date from the database.",
    "what is the award pi id for \"meissa rsv vaccine mv-006\"": 
        "ORAgpt provides the Principal Investigator ID from Emory’s records.",
    "in the sample fort file, tell me about the award emory-choa clinical immunization": 
        "ORAgpt describes the award details, funding, milestones, and reporting requirements."
}

st.title("Rice RBLgpt")
st.subheader("Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad")

user_input = st.text_input("🔍 Ask Rice RBLgpt a question:")

normalized_input = user_input.lower().strip()

if user_input:
    response = response_map.get(normalized_input, 
        f"Simulated RBLgpt response for the 'Pre-Award' workflow. You asked: '{user_input}'")
    st.markdown(f"**💬 Answer:**\n\n{response}")

st.markdown("### 🧠 Example Questions")
st.markdown("""
- What internal documents are needed before submitting a Cayuse proposal at Rice?
- How do I route for Chair/Dean approval?
- How do I initiate a Cayuse submission for NIH?
""")

import streamlit as st

# Banner image (converted to direct access link from Google Drive)
st.image("https://drive.google.com/uc?id=19bb1cBQ5JBY-ntN0E5vqI3pQZ9pmSvpJ", use_column_width=True)

st.title("RBLgpt: Research Business Logic Assistant")

section = st.sidebar.selectbox("Select Section", ["Pre-Award", "Post-Award"])

# Fake upload area
st.subheader("Upload Supporting Documents (Optional)")
uploaded_file = st.file_uploader("Choose a file to simulate upload", type=["pdf", "docx"])

if uploaded_file:
    st.success(f"'{uploaded_file.name}' uploaded successfully. (Note: This is a simulated upload.)")

question = st.text_area("Ask your question:")

def get_simulated_response(section, question):
    if section == "Pre-Award":
        if "chair" in question.lower() or "dean" in question.lower():
            return "Before submitting your proposal in Cayuse, route it through your department chair and then your dean for approval using the internal routing form. Approvals must be documented and uploaded."
        elif "documents" in question.lower():
            return "You’ll need a completed budget, budget justification, scope of work, and internal routing form."
        else:
            return "For Pre-Award questions, ensure your proposal follows Rice’s Cayuse internal guidelines and sponsor-specific requirements."
    elif section == "Post-Award":
        if "burn rate" in question.lower():
            return "You can view your award’s burn rate using the Rice iO dashboard. Navigate to the 'Award Summary' tab and check 'Budget vs. Actuals.'"
        elif "no-cost extension" in question.lower():
            return "Submit a formal NCE request through your iO record. Ensure you include justification, updated timelines, and get PI and departmental approvals."
        elif "allowable" in question.lower() or "expenses" in question.lower():
            return "Allowable expenses must meet OMB Uniform Guidance and sponsor-specific terms. Common categories include personnel, travel, and supplies—but alcohol and administrative salaries are typically unallowable."
        else:
            return "For Post-Award queries, refer to Rice’s iO system SOP and consult your grant’s terms and conditions."
    else:
        return "Please select a section (Pre-Award or Post-Award) for more targeted assistance."

if st.button("Submit"):
    if question:
        response = get_simulated_response(section, question)
        st.write("### Answer:")
        st.info(response)
    else:
        st.warning("Please enter a question.")
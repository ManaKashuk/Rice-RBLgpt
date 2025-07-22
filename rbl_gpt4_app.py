
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Rice RBLgpt", layout="wide")

# Display banner image (Rice Biotech LaunchPad logo)
st.image(
    "https://images.squarespace-cdn.com/content/v1/64e3b8652d51484e88798b28/d6b0de0c-44c7-4796-a116-2ab6da4f7bb0/BiotechLaunchPad.png?format=1500w",
    use_container_width=True
)

# App title and description
st.title("Rice RBLgpt")
st.subheader("Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad")

# Sidebar navigation
section = st.sidebar.radio("Select Section", ("Pre-Award", "Post-Award"))

# Simulated GPT-style response logic
def get_simulated_response(section, question):
    q = question.lower()
    if section == "Pre-Award":
        if "chair" in q or "dean" in q:
            return "Before submitting your proposal in Cayuse, route it through your department chair and then your dean for approval using the internal routing form. Approvals must be documented and uploaded."
        elif "documents" in q:
            return "You’ll need a completed budget, budget justification, scope of work, and internal routing form."
        elif "nih" in q:
            return "To initiate a Cayuse submission for NIH, use the standard SF424 package and follow Rice's internal deadline policy (usually 5 business days prior to sponsor deadline)."
        else:
            return "Please ensure your proposal follows Rice’s Cayuse internal guidelines and sponsor-specific requirements."
    elif section == "Post-Award":
        if "burn rate" in q:
            return "You can view your award’s burn rate using the Rice iO dashboard. Navigate to the 'Award Summary' tab and check 'Budget vs. Actuals.'"
        elif "no-cost extension" in q:
            return "Submit a formal NCE request through your iO record. Ensure you include justification, updated timelines, and get PI and departmental approvals."
        elif "allowable" in q or "expenses" in q:
            return "Allowable expenses must meet OMB Uniform Guidance and sponsor-specific terms. Common categories include personnel, travel, and supplies—but alcohol and administrative salaries are typically unallowable."
        else:
            return "Refer to Rice’s iO system SOP and consult your grant’s terms and conditions for post-award actions."
    return "Please select a valid question category."

# Input form for user question
question = st.text_input("🔍 Ask Rice RBLgpt a question:")

# Generate and display the answer
if question:
    response = get_simulated_response(section, question)
    st.markdown(f"**💬 Answer:**\n\n{response}")

# Example questions section
st.markdown("---")
st.markdown("### 🧠 Example Questions")
if section == "Pre-Award":
    st.markdown("""
- What internal documents are needed before submitting a Cayuse proposal at Rice?
- How do I route for Chair/Dean approval?
- How do I initiate a Cayuse submission for NIH?
""")
else:
    st.markdown("""
- Where can I see budget burn rate for my award?
- How do I request a no-cost extension in iO?
- What expenses are allowable under federal grants?
""")

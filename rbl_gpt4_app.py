
import streamlit as st
from PIL import Image

# Set up app layout
st.set_page_config(page_title="Rice RBLgpt", layout="wide")
st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa;}
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load and display the logo
logo = Image.open("RBLgpt logo.png")  # Make sure this is the file name of your PNG
st.image(logo, width=200)

# Title & Tagline
st.title("Rice RBLgpt")
st.subheader("Empowering Research Integrity and Impact at Rice Biotech LaunchPad")

# Sidebar
section = st.sidebar.selectbox("Select Workflow Section", ["Pre-Award", "Post-Award"])

# Input
question = st.text_input("Ask Rice RBLgpt a question:")

# Simulated Answer Logic
def get_simulated_response(q, section):
    q = q.lower()
    if section == "Pre-Award":
        if "internal documents" in q:
            return "You need internal approvals, budget forms, and sponsor-specific templates uploaded in Cayuse."
        elif "chair" in q or "dean" in q:
            return "Use Cayuse routing to secure Chair and Dean approvals before final submission."
        elif "nih" in q:
            return "Use Cayuse SP to start NIH proposals; refer to Rice’s Cayuse NIH template."
        else:
            return f"Simulated RBLgpt response for Pre-Award. You asked: '{q}'"
    elif section == "Post-Award":
        if "burn rate" in q:
            return "Check the iO dashboard > Budget vs Actual to view burn rate metrics."
        elif "no-cost extension" in q:
            return "Submit a no-cost extension through iO with PI justification and DA routing."
        elif "allowable" in q or "expenses" in q:
            return "Allowable expenses follow Uniform Guidance: typically salary, travel, and supplies. Alcohol and admin costs are not allowable."
        elif "closeout" in q:
            return "Ensure all deliverables submitted, expenses cleared, and iO final reports uploaded within 90–120 days."
        elif "cost transfer" in q or "overspend" in q:
            return "Overspends must be moved to cost-share accounts or unrestricted funds with RCA approval."
        else:
            return f"Simulated RBLgpt response for Post-Award. You asked: '{q}'"
    return "Sorry, I couldn’t understand your question."

# Show response
if question:
    st.markdown("💬 **Answer:**")
    st.write(get_simulated_response(question, section))

# Example Prompt Suggestions
with st.expander("🧠 Example Questions"):
    if section == "Pre-Award":
        st.markdown("""
        - What internal documents are needed before submitting a Cayuse proposal at Rice?
        - How do I route for Chair/Dean approval?
        - How do I initiate a Cayuse submission for NIH?
        """)
    elif section == "Post-Award":
        st.markdown("""
        - Where can I see budget burn rate for my award?
        - How do I request a no-cost extension in iO?
        - What expenses are allowable under federal grants?
        - How do I begin award closeout?
        """)

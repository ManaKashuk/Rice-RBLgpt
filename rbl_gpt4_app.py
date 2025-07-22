
import streamlit as st
from PIL import Image

import streamlit as st

# App Title and Layout
st.set_page_config(page_title="Rice RBLgpt", layout="centered")

# Display logo and title side-by-side (logo left, text right)
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://images.squarespace-cdn.com/content/v1/64e3b8652d51484e88798b28/d6b0de0c-44c7-4796-a116-2ab6da4f7bb0/BiotechLaunchPad.png?format=1500w" width="120" style="margin-right: 20px;"/>
        <div>
            <h1 style="margin-bottom: 0;">Rice RBLgpt</h1>
            <p style="margin-top: 0;">Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for selecting category
category = st.sidebar.selectbox("Select Category", ["Pre-Award", "Post-Award"])

# Question Input
question = st.text_input("🔍 Ask Rice RBLgpt a question:")

# Mock Q&A database
mock_qa = {
    "Pre-Award": {
        "What internal documents are needed before submitting a Cayuse proposal at Rice?":
            "You'll typically need the internal budget, chair approval form, and conflict of interest disclosure.",
        "How do I route for Chair/Dean approval?":
            "Use Cayuse routing — ensure PI certification is complete, then add Chair and Dean as reviewers.",
        "How do I initiate a Cayuse submission for NIH?":
            "Start with the SF424 form in Cayuse, then attach required NIH-specific documents and route internally.",
    },
    "Post-Award": {
        "Where can I see budget burn rate for my award?":
            "Log into iO, go to the Awards module, and select the 'Expenditure Overview' tab.",
        "How do I request a no-cost extension in iO?":
            "Submit a Change Request in iO, include justification, and route through appropriate approvals.",
        "What expenses are allowable under federal grants?":
            "Refer to Uniform Guidance (2 CFR 200) — commonly allowable costs include personnel, supplies, and travel directly tied to project aims.",
    }
}

# Display mock answer
if question:
    answer = mock_qa.get(category, {}).get(question,
        f"Simulated RBLgpt response for the '{category}' workflow. You asked: '{question}'")
    st.markdown("### 💬 Answer:")
    st.write(answer)

# Example questions
st.markdown("### 🧠 Example Questions")
examples = list(mock_qa[category].keys())
for ex in examples:
    st.markdown(f"- {ex}")

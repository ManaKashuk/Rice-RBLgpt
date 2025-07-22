import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# App Title and Layout
st.set_page_config(page_title="Rice RBLgpt", layout="centered")

# Convert local image to base64 string
def get_base64_image(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Load and convert logo
logo_base64 = get_base64_image("RBLgpt logo.png")

# Display the logo and title side-by-side with reduced spacing
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
        <img src="data:image/png;base64,{logo_base64}" width="280" style="margin: 0;" />
        <div style="line-height: 1.2;">
            <h1 style="margin: 0;">Rice RBLgpt</h1>
            <p style="margin: 2px 0 0 0;">Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</p>
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

import streamlit as st
from PIL import Image
# Set the page configuration
st.set_page_config(page_title="Rice RBLgpt", layout="centered")

# Load and display the logo left above the title with adjusted width
logo = Image.open("RBLgpt logo.png")

# Display the logo with fixed width and no extra white space
st.image(logo, width=100)

# Tighten the spacing between logo and title
st.markdown("<h2 style='text-align: left; margin-top: -20px;'>Rice RBLgpt</h1>", unsafe_allow_html=True)

# Subtitle directly below the title
st.markdown("<h5 style='text-align: left; margin-top: -10px;'>Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</h4>", unsafe_allow_html=True)

# File Upload Box
uploaded_file = st.file_uploader("📎 Upload a document", type=["pdf", "docx", "xlsx", "csv"])

if uploaded_file:
    st.success(f"Uploaded file: {uploaded_file.name}")
    
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
import pandas as pd
import streamlit as st

# Load questions
df = pd.read_csv("sample_questions.csv")

category = st.selectbox("Select a section", ["Pre-Award", "Post-Award"])
filtered_df = df[df["Section"] == section]
question = st.selectbox("Choose a question", filtered_df["Question"].tolist())

if question:
    answer = filtered_df[df["Question"] == question]["Answer"].values[0]
    st.markdown(f"**Answer:** {answer}")




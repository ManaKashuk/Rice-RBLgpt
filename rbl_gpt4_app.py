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

import pandas as pd
import streamlit as st

# Load your Q&A data
df = pd.read_csv("sample_questions.csv")

# Let the user choose a category
category = st.selectbox("Select a category", ["Pre-Award", "Post-Award", "Compliance", "System Navigation", "Clinical/Translational Research"])
filtered_df = df[df["Category"] == category]

# Show a text input for the question
user_input = st.text_input("🔍 Ask Rice RBLgpt a question:")

# Suggest matching questions
if user_input:
    # Find closest matches
    suggestions = filtered_df[filtered_df["Question"].str.contains(user_input, case=False, na=False)]

    if not suggestions.empty:
        st.markdown("**Suggestions:**")
        for idx, row in suggestions.iterrows():
            if st.button(row["Question"]):  # Each suggestion is a button
                st.markdown(f"**Answer:** {row['Answer']}")
   else:
        # No matches found — try to suggest the best category
        all_questions = df["Question"].tolist()
        closest_matches = get_close_matches(user_input, all_questions, n=1, cutoff=0.3)

        if closest_matches:
            best_match = closest_matches[0]
            matched_category = df[df["Question"] == best_match]["Category"].values[0]
            st.info(f"No exact match found, but this question may belong to **{matched_category}** category.\n\nDid you mean:\n- {best_match}")
        else:
            st.info("No similar questions found. Please try rephrasing.")





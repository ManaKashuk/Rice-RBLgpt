import streamlit as st
from PIL import Image
# Set the page configuration
st.set_page_config(page_title="Rice RBLgpt", layout="centered")

# Load and display the logo left above the title with adjusted width
logo = Image.open("RBLgpt_logo.png")

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
from difflib import get_close_matches

# Load your Q&A data
df = pd.read_csv("sample_questions.csv")

# Let the user choose a category
category = st.selectbox("Select a category", ["Pre-Award", "Post-Award", "Compliance", "System Navigation", "Clinical/Translational Research"])
filtered_df = df[df["Category"] == category]

# Show a text input for the question
user_input = st.text_input("🔍 Ask Rice RBLgpt a question:")

# Suggest matching questions from selected category
if user_input:
    suggestions = filtered_df[filtered_df["Question"].str.contains(user_input, case=False, na=False)]

    if not suggestions.empty:
        st.markdown("**Suggestions:**")
        for idx, row in suggestions.iterrows():
            if st.button(row["Question"]):
                st.markdown(f"**Answer:** {row['Answer']}")
    else:
        # No matches in selected category — try to suggest best overall match
        all_questions = df["Question"].tolist()
        closest_matches = get_close_matches(user_input, all_questions, n=1, cutoff=0.6)  # Higher cutoff = more confident

        if closest_matches:
            best_match = closest_matches[0]
            matched_row = df[df["Question"] == best_match].iloc[0]
            matched_category = matched_row["Category"]
            matched_answer = matched_row["Answer"]

            st.markdown(f"**Note:** Your question seems related to the **{matched_category}** category.")
            st.markdown(f"**Suggested Question:** {best_match}")
            st.markdown(f"**Answer:** {matched_answer}")
        else:
            st.info("No similar questions found. Please try rephrasing.")

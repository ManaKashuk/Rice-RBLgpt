import streamlit as st
from PIL import Image
import pandas as pd
from difflib import get_close_matches

# --- Page Setup ---
st.set_page_config(page_title="Rice RBLgpt", layout="centered")

# Load and display logo at the top
logo = Image.open("RBLgpt logo.png")
st.image(logo, width=100)

# Title and subtitle
st.markdown("<h2 style='text-align: left; margin-top: -20px;'>Rice RBLPgpt</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; margin-top: -10px;'>Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</h5>", unsafe_allow_html=True)

st.markdown("🧠 _RBLgpt is trained to respond like a Rice research admin based on SOP guidance._")

# Upload file (optional)
uploaded_file = st.file_uploader("📎 Upload a document", type=["pdf", "docx", "xlsx", "csv"])
if uploaded_file:
    st.success(f"Uploaded file: {uploaded_file.name}")

# Load questions/answers data
df = pd.read_csv("sample_questions.csv")

# Initialize session state variables if not set
if "messages" not in st.session_state:
    st.session_state.messages = []
if "awaiting_confirmation" not in st.session_state:
    st.session_state.awaiting_confirmation = False
if "typed_question" not in st.session_state:
    st.session_state.typed_question = ""

# Helper function to show assistant's answer with logo
def show_answer_with_logo(answer_text):
    col1, col2 = st.columns([1, 10])
    with col1:
        st.image(logo, width=40)  # Use the same logo loaded at the top
    with col2:
        st.markdown(f"**Answer:** {answer_text}")

# Category selection
category = st.selectbox(
    "📂 Select a category to guide your question:",
    df["Category"].unique()
)

filtered_df = df[df["Category"] == category]

# Show some example questions to the user
if not st.session_state.typed_question:
    st.markdown("💬 Try asking:")
    for q in filtered_df["Question"].head(3):
        st.markdown(f"- {q}")

# Suggested questions as buttons
st.markdown("💡 **Suggested Questions (click to autofill)**")

selected_question = st.selectbox(
    "Choose a suggested question from this category:",
    options=[""] + filtered_df["Question"].tolist(),
    index=0,
    key="suggested_question_select"
)

# When user selects a question, autofill the input box
if selected_question and selected_question != "":
    st.session_state.typed_question = selected_question
    st.experimental_rerun()  # reload with the selected question in the input

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            # Show answer with logo inside chat message
            show_answer_with_logo(msg["content"].replace("**Answer:** ", ""))

# Text input for user's question
user_input = st.text_input(
    "Ask your question...",
    value=st.session_state.get("typed_question", ""),
    key="typed_question_input"
)

# Submit button
if st.button("💬 Submit") and user_input.strip():
    question = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": question})

    # Exact match in filtered_df
    match_row = filtered_df[filtered_df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})
        show_answer_with_logo(answer)
        st.session_state.awaiting_confirmation = False
        st.session_state.typed_question = ""
    else:
        # If no exact match, suggest close matches
        all_questions = df["Question"].tolist()
        close_matches = get_close_matches(question, all_questions, n=3, cutoff=0.6)

        if close_matches:
            best_match = close_matches[0]
            matched_row = df[df["Question"] == best_match].iloc[0]
            st.session_state.awaiting_confirmation = True

            st.markdown(f"🤔 Did you mean:\n> **{best_match}**\n\n_Category: {matched_row['Category']}_")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, show answer", key="confirm_yes"):
                    answer = matched_row["Answer"]
                    st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})
                    show_answer_with_logo(answer)
                    st.session_state.awaiting_confirmation = False
                    st.session_state.typed_question = ""
            with col2:
                if st.button("❌ No, try again", key="confirm_no"):
                    st.info("Okay, please try rephrasing your question.")
                    st.session_state.awaiting_confirmation = False
                    st.session_state.typed_question = ""

        else:
            st.info("Sorry, I couldn't find a related question. Please try rephrasing.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Sorry, I couldn't find a related question. Please try rephrasing."
            })

# Optional: autocomplete suggestions while typing
if st.session_state.typed_question:
    matches = filtered_df[filtered_df["Question"].str.contains(st.session_state.typed_question, case=False, na=False)]
    if not matches.empty:
        st.markdown("**🔎 Suggestions:**")
        for i, q in enumerate(matches["Question"].head(5)):
            if st.button(q, key=f"suggestion_btn_{i}"):
                st.session_state.typed_question = q # ❌ THIS LINE CAUSES CRASH

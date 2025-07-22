import streamlit as st
import pandas as pd
from PIL import Image
from difflib import get_close_matches

# Set the page configuration
st.set_page_config(page_title="Rice RBLgpt", layout="centered")

# Load and display the logo
try:
    logo = Image.open("RBLgpt logo.png")
    st.image(logo, width=100)
except FileNotFoundError:
    st.warning("Logo file 'RBLgpt logo.png' not found.")

# Display title and subtitle
st.markdown("<h2 style='text-align: left; margin-top: -20px;'>Rice RBLgpt</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; margin-top: -10px;'>Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</h5>", unsafe_allow_html=True)

# File Upload Box
uploaded_file = st.file_uploader("📎 Upload a document", type=["pdf", "docx", "xlsx", "csv"])
if uploaded_file:
    st.success(f"Uploaded file: {uploaded_file.name}")

# Load data
try:
    df = pd.read_csv("sample_questions.csv")
except FileNotFoundError:
    st.error("The file 'sample_questions.csv' is missing. Please upload it or place it in the app directory.")
    st.stop()

# Initialize session state
for key, default in {
    "messages": [],
    "suggested_question": None,
    "suggested_category": None,
    "suggested_answer": None,
    "awaiting_confirmation": False,
    "submitted": False,
    "typed_question": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def submit_question():
    st.session_state.submitted = True

# Category dropdown
category = st.selectbox(
    "📂 Select a category to guide your question:",
    ["Pre-Award", "Post-Award", "Compliance", "System Navigation", "Clinical/Translational Research"]
)
filtered_df = df[df["Category"] == category]

# Download chat history button
if st.session_state.messages:
    chat_text = ""
    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "Rice RBLgpt"
        chat_text += f"{role}: {msg['content']}\n\n"

    st.download_button(
        label="📥 Download Chat History",
        data=chat_text,
        file_name="rblgpt_chat_history.txt",
        mime="text/plain"
    )

# Suggested questions from category as buttons
with st.expander("💡 Suggested questions from this category", expanded=False):
    for i, question in enumerate(filtered_df["Question"].tolist()):
        if st.button(question, key=f"category_suggestion_btn_{i}"):
            answer = filtered_df[filtered_df["Question"] == question]["Answer"].values[0]
            with st.chat_message("assistant"):
                st.markdown(f"**Answer:** {answer}")
            st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box and submit button
user_input = st.text_input("Ask your question...", key="typed_question", on_change=submit_question)
submit = st.button("💬 Submit", on_click=submit_question)

# Process input on submission
if st.session_state.submitted and st.session_state.typed_question:
    st.session_state.submitted = False
    user_input = st.session_state.typed_question.strip()
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Exact match in chosen category
    match_row = filtered_df[filtered_df["Question"].str.lower() == user_input.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        with st.chat_message("assistant"):
            st.markdown(f"**Answer:** {answer}")
        st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})
        st.session_state.awaiting_confirmation = False

    # No exact match — suggest closest question with confirmation
    elif not st.session_state.awaiting_confirmation:
        all_questions = df["Question"].tolist()
        close_matches = get_close_matches(user_input, all_questions, n=1, cutoff=0.6)

        if close_matches:
            best_match = close_matches[0]
            matched_row = df[df["Question"] == best_match].iloc[0]

            st.session_state.suggested_question = best_match
            st.session_state.suggested_category = matched_row["Category"]
            st.session_state.suggested_answer = matched_row["Answer"]
            st.session_state.awaiting_confirmation = True

            with st.chat_message("assistant"):
                st.markdown(f"🤔 I couldn’t find an exact match in **{category}**, but this might help:")
                st.markdown(f"Did you mean:\n> **{best_match}**\n\n_Category: {st.session_state.suggested_category}_")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, show answer", key="confirm_yes"):
                        with st.chat_message("assistant"):
                            st.markdown(f"**Answer:** {st.session_state.suggested_answer}")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**Answer:** {st.session_state.suggested_answer}"
                        })
                        st.session_state.awaiting_confirmation = False
                        st.session_state.typed_question = ""
                with col2:
                    if st.button("❌ No, try again", key="confirm_no"):
                        with st.chat_message("assistant"):
                            st.info("Okay, feel free to rephrase your question.")
                        st.session_state.awaiting_confirmation = False
                        st.session_state.typed_question = ""

        else:
            with st.chat_message("assistant"):
                st.info("Sorry, I couldn't find a related question. Please try rephrasing.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Sorry, I couldn't find a related question. Please try rephrasing."
            })

# Autocomplete-like suggestions below input
if st.session_state.typed_question:
    matches = filtered_df[filtered_df["Question"].str.contains(st.session_state.typed_question, case=False, na=False)]
    if not matches.empty:
        st.markdown("**🔎 Suggestions:**")
        for i, q in enumerate(matches["Question"].head(5)):
        if st.button(q, key=f"suggestion_btn_{i}"):
            st.session_state.typed_question = q  # ✅ This is fine because q is defined in the loop

            


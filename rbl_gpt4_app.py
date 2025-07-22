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
from difflib import get_close_matches

# Load data
df = pd.read_csv("sample_questions.csv")

# Set up session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggested_question" not in st.session_state:
    st.session_state.suggested_question = None
if "suggested_category" not in st.session_state:
    st.session_state.suggested_category = None
if "suggested_answer" not in st.session_state:
    st.session_state.suggested_answer = None
if "awaiting_confirmation" not in st.session_state:
    st.session_state.awaiting_confirmation = False

# CATEGORY DROPDOWN
category = st.selectbox(
    "📂 Select a category to guide your question:",
    ["Pre-Award", "Post-Award", "Compliance", "System Navigation", "Clinical/Translational Research"]
)
filtered_df = df[df["Category"] == category]

# AUTOCOMPLETE SUGGESTIONS
with st.expander("💡 Suggested questions from this category", expanded=False):
    for question in filtered_df["Question"].tolist():
        if st.button(question):
            answer = filtered_df[filtered_df["Question"] == question]["Answer"].values[0]
            with st.chat_message("assistant"):
                st.markdown(f"**Answer:** {answer}")
            st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})

# DISPLAY CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# USER INPUT + AUTOCOMPLETE
user_input = st.text_input("Ask your question...", key="typed_question")

# Live suggestions while typing
if user_input:
    matches = filtered_df[filtered_df["Question"].str.contains(user_input, case=False, na=False)]
    if not matches.empty:
        st.markdown("**🔎 Suggestions:**")
        for q in matches["Question"].head(5):
            if st.button(q):
                answer = filtered_df[filtered_df["Question"] == q]["Answer"].values[0]
                with st.chat_message("assistant"):
                    st.markdown(f"**Answer:** {answer}")
                st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})

submit = st.button("💬 Submit")

if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    match_row = filtered_df[filtered_df["Question"].str.lower() == user_input.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        with st.chat_message("assistant"):
            st.markdown(f"**Answer:** {answer}")
        st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})
        st.session_state.awaiting_confirmation = False

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
                    if st.button("✅ Yes, show answer"):
                        with st.chat_message("assistant"):
                            st.markdown(f"**Answer:** {st.session_state.suggested_answer}")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**Answer:** {st.session_state.suggested_answer}"
                        })
                        st.session_state.awaiting_confirmation = False
                with col2:
                    if st.button("❌ No, try again"):
                        with st.chat_message("assistant"):
                            st.info("Okay, feel free to rephrase your question.")
                        st.session_state.awaiting_confirmation = False
        else:
            with st.chat_message("assistant"):
                st.info("Sorry, I couldn't find a related question. Please try rephrasing.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Sorry, I couldn't find a related question. Please try rephrasing."
            })
import io

# Convert chat messages to plain text
if st.session_state.messages:
    chat_text = ""
    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "Rice RBLgpt"
        chat_text += f"{role}: {msg['content']}\n\n"

    # Create download button
    st.download_button(
        label="📥 Download Chat History",
        data=chat_text,
        file_name="rblgpt_chat_history.txt",
        mime="text/plain"
    )
def submit_question():
    st.session_state.submitted = True

# Text input with on_change triggers when user presses Enter
user_input = st.text_input("Ask your question...", key="typed_question", on_change=submit_question)

# Submit button
submit = st.button("💬 Submit", on_click=submit_question)

# Check if submitted by either Enter or button
if st.session_state.get("submitted", False) and user_input:
    # Reset submit flag
    st.session_state.submitted = False

    # Your existing logic here to handle the question
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ... rest of matching and response logic ...

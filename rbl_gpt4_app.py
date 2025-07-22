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

# Load your Q&A data
df = pd.read_csv("sample_questions.csv")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggested_question" not in st.session_state:
    st.session_state.suggested_question = None
    st.session_state.suggested_category = None
    st.session_state.suggested_answer = None
    st.session_state.awaiting_confirmation = False

# Display past chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
user_input = st.chat_input("Ask a question about research support at Rice...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Search for exact match
    match_row = df[df["Question"].str.lower() == user_input.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        with st.chat_message("assistant"):
            st.markdown(f"**Answer:** {answer}")
        st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})

    elif not st.session_state.awaiting_confirmation:
        # No exact match, try finding closest match
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
                st.markdown(f"🤔 I couldn't find an exact match, but your question may belong to the **{st.session_state.suggested_category}** category.")
                st.markdown(f"Did you mean:\n> **{st.session_state.suggested_question}**")

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
                    if st.button("❌ No, that's not it"):
                        with st.chat_message("assistant"):
                            st.info("Okay, feel free to rephrase your question.")
                        st.session_state.awaiting_confirmation = False
        else:
            with st.chat_message("assistant"):
                st.info("Sorry, I couldn’t find anything similar. Please try rephrasing.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Sorry, I couldn’t find anything similar. Please try rephrasing."
            })

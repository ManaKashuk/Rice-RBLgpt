
import streamlit as st
from PIL import Image
import pandas as pd
from difflib import get_close_matches

# Set the page configuration
st.set_page_config(page_title="Rice RBLPgpt", layout="centered")

# Display the logo
logo = Image.open("RBLgpt logo.png")
st.image(logo, width=100)

# Title and subtitle
st.markdown("<h2 style='text-align: left; margin-top: -20px;'>Rice RBLPgpt</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; margin-top: -10px;'>Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</h5>", unsafe_allow_html=True)

# Role priming banner
st.markdown("🧠 _RBLgpt is trained to respond like a Rice research admin based on SOP guidance._")

# File uploader
uploaded_file = st.file_uploader("📎 Upload a document", type=["pdf", "docx", "xlsx", "csv"])
if uploaded_file:
    st.success(f"Uploaded file: {uploaded_file.name}")

# Load data
df = pd.read_csv("sample_questions.csv")

# Initialize session state
for key in ["messages", "suggested_question", "suggested_category", "suggested_answer", "awaiting_confirmation", "submitted", "typed_question"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "messages" else ""

# Handle submission
def submit_question():
    st.session_state.submitted = True

# Category dropdown
category = st.selectbox(
    "📂 Select a category to guide your question:",
    ["Pre-Award", "Post-Award", "Compliance", "System Navigation", "Clinical/Translational Research"]
)
filtered_df = df[df["Category"] == category]

# Download chat history
if st.session_state.messages:
    chat_text = "\n\n".join(f"{'You' if m['role']=='user' else 'Rice RBLgpt'}: {m['content']}" for m in st.session_state.messages)
    st.download_button("📥 Download Chat History", data=chat_text, file_name="rblgpt_chat_history.txt", mime="text/plain")

# Suggested default questions
if not st.session_state.typed_question:
    st.markdown("💬 Try asking:")
    examples = filtered_df["Question"].head(3).tolist()
    for example in examples:
        st.markdown(f"- {example}")

# Suggested questions as buttons
with st.expander("💡 Suggested questions from this category", expanded=False):
    for i, question in enumerate(filtered_df["Question"].tolist()):
        if st.button(question, key=f"cat_btn_{i}"):
            answer = filtered_df[filtered_df["Question"] == question]["Answer"].values[0]
            with st.chat_message("assistant"):
                st.markdown(f"**Answer:** {answer}")
            st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input + submit
user_input = st.text_input("Ask your question...", key="typed_question", on_change=submit_question)
submit = st.button("💬 Submit", on_click=submit_question)

if st.session_state.submitted and user_input:
    st.session_state.submitted = False
    question = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    match_row = filtered_df[filtered_df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        with st.chat_message("assistant"):
            st.markdown(f"**Answer:** {answer}")
        st.session_state.messages.append({"role": "assistant", "content": f"**Answer:** {answer}"})
        st.session_state.awaiting_confirmation = False
    elif not st.session_state.awaiting_confirmation:
        all_questions = df["Question"].tolist()
        close_matches = get_close_matches(question, all_questions, n=3, cutoff=0.6)
        if close_matches:
            best_match = close_matches[0]
            matched_row = df[df["Question"] == best_match].iloc[0]
            st.session_state.suggested_question = best_match
            st.session_state.suggested_category = matched_row["Category"]
            st.session_state.suggested_answer = matched_row["Answer"]
            st.session_state.awaiting_confirmation = True
            with st.chat_message("assistant"):
                st.markdown(f"🤔 Did you mean:\n> **{best_match}**\n\n_Category: {st.session_state.suggested_category}_")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, show answer", key="confirm_yes"):
                        with st.chat_message("assistant"):
                            st.markdown(f"**Answer:** {st.session_state.suggested_answer}")
                        st.session_state.messages.append({
                            "role": "assistant", "content": f"**Answer:** {st.session_state.suggested_answer}"
                        })
                        st.session_state.awaiting_confirmation = False
                        st.session_state.typed_question = ""
                with col2:
                    if st.button("❌ No, try again", key="confirm_no"):
                        st.info("Okay, feel free to rephrase your question.")
                        st.session_state.awaiting_confirmation = False
                        st.session_state.typed_question = ""
        else:
            with st.chat_message("assistant"):
                st.info("Sorry, I couldn't find a related question. Please try rephrasing.")
            st.session_state.messages.append({
                "role": "assistant", "content": "Sorry, I couldn't find a related question. Please try rephrasing."
            

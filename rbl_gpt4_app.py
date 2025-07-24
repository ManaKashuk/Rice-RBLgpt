import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image
import io

# --- Setup ---
st.set_page_config(page_title="Rice RBLgpt", layout="centered")
logo = Image.open("RBLgpt logo.png")
st.image(logo, width=100)
st.markdown("<h2>Rice RBLgpt</h2>", unsafe_allow_html=True)
st.markdown("_Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad_")

# --- Load CSV ---
df = pd.read_csv("sample_questions.csv")

# --- Category Selection ---
category = st.selectbox("📂 Select a category:", df["Category"].unique())
filtered_df = df[df["Category"] == category]
category_questions = filtered_df["Question"].tolist()

# --- Session State Setup ---
for key in ["chat_history", "typed_question", "suggested_q", "suggested_ans", "suggested_cat", "awaiting_confirmation"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "history" in key else ""

# --- Show Chat Messages ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image(logo, width=40)
            with col2:
                st.markdown(f"**Answer:** {msg['content']}")
        else:
            st.markdown(msg["content"])

# --- Main Input Prompt ---
question = st.chat_input("Start typing...")
if question:
    question = question.strip()
    st.session_state.chat_history.append({"role": "user", "content": question})

    # --- Check for Exact Match ---
    match_row = df[df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    # --- Try Close Match ---
    all_questions = df["Question"].tolist()
    close_matches = get_close_matches(question, all_questions, n=1, cutoff=0.5)

    if close_matches:
        best_match = close_matches[0]
        match_row = df[df["Question"] == best_match].iloc[0]
        st.session_state.suggested_q = best_match
        st.session_state.suggested_ans = match_row["Answer"]
        st.session_state.suggested_cat = match_row["Category"]
        st.session_state.awaiting_confirmation = True
        st.rerun()

# --- Handle Suggested Answer ---
if st.session_state.awaiting_confirmation:
    with st.chat_message("assistant"):
        st.markdown(f"🤔 Did you mean:\n> **{st.session_state.suggested_q}**\n\n_Category: {st.session_state.suggested_cat}_")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, show answer", key="yes_confirm"):
                st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.suggested_ans})
                st.session_state.awaiting_confirmation = False
                st.session_state.suggested_q = ""
                st.rerun()
        with col2:
            if st.button("❌ No, ask again", key="no_confirm"):
                st.session_state.awaiting_confirmation = False
                st.session_state.suggested_q = ""
                st.session_state.suggested_ans = ""
                st.rerun()

# --- Download Chat History ---
if st.session_state.chat_history:
    chat_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
    buffer = io.StringIO(chat_text)
    st.download_button("📥 Download Chat History", buffer, file_name="chat_history.txt", mime="text/plain")

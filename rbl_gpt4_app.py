
import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image
from datetime import datetime

# ---------- Config & Logo ----------
st.set_page_config(page_title="Rice RBLgpt", layout="centered")

logo = Image.open("RBLgpt logo.png")
st.image(logo, width=100)
st.markdown("<h1>Rice RBLgpt</h1>", unsafe_allow_html=True)
st.markdown("_Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad_")
st.markdown("🧠 _RBLgpt is trained to respond like a Rice Biotech LaunchPad Research Admin based on SOP guidance._")

# ---------- Load CSV ----------
df = pd.read_csv("sample_questions.csv")

# ---------- Session Setup ----------
for key, default in {
    "chat_history": [],
    "awaiting_confirmation": False,
    "suggested_q": "",
    "suggested_ans": "",
    "suggested_cat": "",
    "typed_question": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------- Step 1: Category Selection ----------
category = st.selectbox("📂 Select a category:", df["Category"].unique())
filtered_df = df[df["Category"] == category]
category_questions = filtered_df["Question"].tolist()

# ---------- Step 2: Ask a Question ----------
st.markdown("💬 **Type your question** (suggestions will appear as you type):")

question = st.autocomplete(
    label="Your question:",
    options=category_questions,
    value=st.session_state.typed_question,
    key="typed_input"
)

submit = st.button("Submit")

# ---------- Step 3: Process the Question ----------
if submit and question.strip():
    question = question.strip()
    st.session_state.typed_question = ""

    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    match_row = filtered_df[filtered_df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        with st.chat_message("assistant"):
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image(logo, width=40)
            with col2:
                st.markdown(f"**Answer:** {answer}")
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        all_questions = df["Question"].tolist()
        close_matches = get_close_matches(question, all_questions, n=1, cutoff=0.6)

        if close_matches:
            best_match = close_matches[0]
            match = df[df["Question"] == best_match].iloc[0]
            st.session_state.suggested_q = best_match
            st.session_state.suggested_ans = match["Answer"]
            st.session_state.suggested_cat = match["Category"]
            st.session_state.awaiting_confirmation = True
        else:
            with st.chat_message("assistant"):
                st.info("❌ Sorry, I couldn't find a similar question. Please rephrase.")

# ---------- Step 4: Handle Confirmation ----------
if st.session_state.awaiting_confirmation:
    with st.chat_message("assistant"):
        st.markdown(f"🤔 Did you mean:\n> **{st.session_state.suggested_q}**\n\n_Category: {st.session_state.suggested_cat}_")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, show answer", key="yes_confirm"):
                with st.chat_message("assistant"):
                    col1, col2 = st.columns([1, 10])
                    with col1:
                        st.image(logo, width=40)
                    with col2:
                        st.markdown(f"**Answer:** {st.session_state.suggested_ans}")
                st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.suggested_ans})
                st.session_state.awaiting_confirmation = False
                st.session_state.suggested_q = ""
                st.session_state.suggested_ans = ""
        with col2:
            if st.button("❌ No, ask again", key="no_confirm"):
                st.info("Okay, feel free to rephrase your question.")
                st.session_state.awaiting_confirmation = False
                st.session_state.suggested_q = ""
                st.session_state.suggested_ans = ""

# ---------- Step 5: File Upload ----------
st.divider()
st.markdown("📎 **Upload a document**")
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "xlsx", "csv"])
if uploaded_file:
    st.success(f"Uploaded file: {uploaded_file.name}")

# ---------- Step 6: Download Chat History ----------
st.divider()
st.markdown("📥 **Download Chat History**")
if st.session_state.chat_history:
    chat_lines = []
    for msg in st.session_state.chat_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        chat_lines.append(f"{role}: {msg['content']}")
    chat_text = "\n\n".join(chat_lines)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{timestamp}.txt"
    st.download_button("Download Chat History", chat_text, file_name=filename)
    

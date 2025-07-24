import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image
import io

# ---------- Config & Logo ----------
st.set_page_config(page_title="Rice RBLgpt", layout="centered")
logo = Image.open("RBLgpt logo.png")
st.image(logo, width=100)
st.markdown("<h2>Rice RBLgpt</h2>", unsafe_allow_html=True)
st.markdown("_Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad_")
st.markdown("🧠 _RBLgpt is trained to respond like a Rice Biotech LaunchPad Research Admin based on SOP guidance._")

# ---------- Load CSV ----------
df = pd.read_csv("sample_questions.csv")

# ---------- Session Setup ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "awaiting_confirmation" not in st.session_state:
    st.session_state.awaiting_confirmation = False
if "suggested_q" not in st.session_state:
    st.session_state.suggested_q = ""
if "suggested_ans" not in st.session_state:
    st.session_state.suggested_ans = ""
if "suggested_cat" not in st.session_state:
    st.session_state.suggested_cat = ""
if "typed_question" not in st.session_state:
    st.session_state.typed_question = ""

# ---------- Step 1: Category Selection ----------
category = st.selectbox("📂 Select a category:", df["Category"].unique())
filtered_df = df[df["Category"] == category]
category_questions = filtered_df["Question"].tolist()

# ---------- Step 2: Input Box & Suggestions ----------
st.markdown("💬 **Type your question:**")
question = st.text_input("Start typing...", value=st.session_state.typed_question, key="question_input")
st.session_state.typed_question = question

# Suggestions from selected category
suggestions = [q for q in category_questions if question.lower() in q.lower() and q.lower() != question.lower()]
if suggestions:
    selected = st.selectbox("🔍 Suggestions (click to autofill):", suggestions, key="suggestion_select")
    if selected:
        st.session_state.typed_question = selected
        st.rerun()

submit = st.button("Submit")

# ---------- Step 3: Process the Question ----------
if submit and question.strip():
    question = question.strip()
    st.session_state.typed_question = ""

    # Store user message
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Check exact match in selected category
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

    # No exact match — try to infer category & suggest close match
    else:
        all_questions = df["Question"].tolist()
        close_matches = get_close_matches(question, all_questions, n=1, cutoff=0.6)

        # Try to guess category by similarity
        guessed_category = None
        for cat in df["Category"].unique():
            if any(get_close_matches(question, df[df["Category"] == cat]["Question"].tolist(), n=1, cutoff=0.4)):
                guessed_category = cat
                break

        if guessed_category:
            st.session_state.suggested_cat = guessed_category
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"🗂 Based on your question, it might relate to the **{guessed_category}** category."
            })

        if close_matches:
            best_match = close_matches[0]
            match = df[df["Question"] == best_match].iloc[0]
            st.session_state.suggested_q = best_match
            st.session_state.suggested_ans = match["Answer"]
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

# ---------- Step 5: Download Chat History ----------
if st.session_state.chat_history:
    def generate_chat_text():
        text = ""
        for msg in st.session_state.chat_history:
            role = "You" if msg["role"] == "user" else "RBLgpt"
            text += f"{role}: {msg['content']}\n\n"
        return text

    chat_text = generate_chat_text()
    chat_bytes = io.BytesIO(chat_text.encode("utf-8"))

    st.divider()
    st.download_button(
        label="📥 Download Chat History",
        data=chat_bytes,
        file_name="RBLgpt_chat_history.txt",
        mime="text/plain"
    )

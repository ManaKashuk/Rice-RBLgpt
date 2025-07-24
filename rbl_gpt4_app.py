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
st.markdown("🧠 _Trained to respond like a Rice Biotech LaunchPad Research Admin based on SOP guidance._")

# ---------- Load CSV ----------
df = pd.read_csv("sample_questions.csv")

# ---------- Session State ----------
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
if "extra_suggestion" not in st.session_state:
    st.session_state.extra_suggestion = ""
if "extra_suggestion_cat" not in st.session_state:
    st.session_state.extra_suggestion_cat = ""

# ---------- Step 1: Category Selection ----------
category = st.selectbox("📂 Select a category:", ["All Categories"] + sorted(df["Category"].unique()))
selected_df = df if category == "All Categories" else df[df["Category"] == category]

# ---------- Display Chat ----------
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user", avatar=None):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar=None):
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image(logo, width=40)
            with col2:
                st.markdown(msg["content"])

# ---------- Chat Input ----------
prompt = st.chat_input("Start typing your question...")
if prompt:
    question = prompt.strip()
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Reset suggestions
    st.session_state.awaiting_confirmation = False
    st.session_state.suggested_q = ""
    st.session_state.suggested_ans = ""
    st.session_state.suggested_cat = ""
    st.session_state.extra_suggestion = ""
    st.session_state.extra_suggestion_cat = ""

    # Search for exact match in selected category
    match_row = selected_df[selected_df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        st.session_state.chat_history.append({"role": "assistant", "content": f"**Answer:** {answer}"})

    else:
        # No exact match in selected category → try suggestions
        all_questions = df["Question"].tolist()

        # Find best match in ALL categories
        best_global_match = get_close_matches(question, all_questions, n=1, cutoff=0.6)
        # Find best match in CURRENT category
        best_local_match = get_close_matches(question, selected_df["Question"].tolist(), n=1, cutoff=0.6)

        # Guess correct category based on global match
        guessed_category = None
        if best_global_match:
            best_match_text = best_global_match[0]
            guessed_category = df[df["Question"] == best_match_text].iloc[0]["Category"]

        # Prepare messages for user
        response_text = ""
        if guessed_category and guessed_category != category:
            response_text += f"🗂 Your question might belong to **{guessed_category}** category.\n\n"

        if best_local_match:
            local_match_text = best_local_match[0]
            local_row = selected_df[selected_df["Question"] == local_match_text].iloc[0]
            st.session_state.suggested_q = local_match_text
            st.session_state.suggested_ans = local_row["Answer"]
            st.session_state.suggested_cat = category
            response_text += f"🤔 Did you mean (in this category): **{local_match_text}**?"
            st.session_state.awaiting_confirmation = True

        if best_global_match and (not best_local_match or best_global_match[0] != best_local_match[0]):
            global_row = df[df["Question"] == best_global_match[0]].iloc[0]
            st.session_state.extra_suggestion = best_global_match[0]
            st.session_state.extra_suggestion_cat = guessed_category
            if not response_text:
                response_text += f"🤔 Did you mean: **{best_global_match[0]}**? (_Category: {guessed_category}_)"
                st.session_state.suggested_q = best_global_match[0]
                st.session_state.suggested_ans = global_row["Answer"]
                st.session_state.awaiting_confirmation = True

        if response_text:
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": "I couldn't find a close match. Please try rephrasing."})

    st.rerun()

# ---------- If awaiting confirmation, show Yes/No buttons ----------
if st.session_state.awaiting_confirmation:
    with st.chat_message("assistant", avatar=None):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, show answer"):
                st.session_state.chat_history.append({"role": "assistant", "content": f"**Answer:** {st.session_state.suggested_ans}"})
                st.session_state.awaiting_confirmation = False
                st.session_state.suggested_q = ""
                st.session_state.suggested_ans = ""
                st.rerun()
        with col2:
            if st.button("❌ No, ask again"):
                st.session_state.awaiting_confirmation = False
                st.session_state.suggested_q = ""
                st.session_state.suggested_ans = ""
                st.rerun()

# ---------- Download Chat ----------
if st.session_state.chat_history:
    chat_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
    buffer = io.StringIO(chat_text)
    st.download_button("📥 Download Chat", buffer, file_name="chat_history.txt", mime="text/plain")

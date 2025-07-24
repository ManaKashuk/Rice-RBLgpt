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

# ---------- Display Chat ----------
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user", avatar=None):  # No user icon
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar=None):  # Custom assistant UI
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image(logo, width=40)
            with col2:
                st.markdown(msg["content"])

# ---------- New Question Input ----------
prompt = st.chat_input("Ask a question...")
if prompt:
    question = prompt.strip()
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Check for exact match
    match_row = df[df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        st.session_state.chat_history.append({"role": "assistant", "content": f"**Answer:** {answer}"})
    else:
        # Check for close match
        all_questions = df["Question"].tolist()
        close_matches = get_close_matches(question, all_questions, n=1, cutoff=0.6)

        # Guess category
        guessed_category = None
        for cat in df["Category"].unique():
            if any(get_close_matches(question, df[df["Category"] == cat]["Question"].tolist(), n=1, cutoff=0.4)):
                guessed_category = cat
                break

        # Add category hint
        if guessed_category:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"🗂 This might belong to the **{guessed_category}** category."
            })

        # If we have a suggestion
        if close_matches:
            best_match = close_matches[0]
            match = df[df["Question"] == best_match].iloc[0]
            st.session_state.suggested_q = best_match
            st.session_state.suggested_ans = match["Answer"]
            st.session_state.suggested_cat = match["Category"]
            st.session_state.awaiting_confirmation = True

            # Add suggestion inside the chat flow
            suggestion_text = f"🤔 Did you mean:\n**{best_match}**\n\n_Category: {match['Category']}_"
            st.session_state.chat_history.append({"role": "assistant", "content": suggestion_text})
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": "I couldn't find an exact match. Please rephrase."})

    st.rerun()

# ---------- If awaiting confirmation, show buttons inline ----------
if st.session_state.awaiting_confirmation:
    with st.chat_message("assistant", avatar=None):
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Yes, show answer"):
                st.session_state.chat_history.append({"role": "assistant", "content": f"**Answer:** {st.session_state.suggested_ans}"})
                st.session_state.awaiting_confirmation = False
                st.session_state.suggested_q = ""
                st.session_state.suggested_ans = ""
                st.session_state.suggested_cat = ""
                st.rerun()
        with col2:
            if st.button("❌ No, ask again"):
                st.session_state.awaiting_confirmation = False
                st.session_state.suggested_q = ""
                st.session_state.suggested_ans = ""
                st.session_state.suggested_cat = ""
                st.rerun()

# ---------- Download Chat History ----------
if st.session_state.chat_history:
    chat_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
    buffer = io.StringIO(chat_text)
    st.download_button("📥 Download Chat", buffer, file_name="chat_history.txt", mime="text/plain")

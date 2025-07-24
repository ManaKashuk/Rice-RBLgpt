import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image

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

# ---------- Step 1: Category Selection ----------
category = st.selectbox("📂 Select a category:", ["All Categories"] + sorted(df["Category"].unique()))
selected_df = df if category == "All Categories" else df[df["Category"] == category]

# ---------- Display Chat ----------
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        with st.chat_message("user", avatar=None):  # No default icon
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar=None):  # Custom layout
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image(logo, width=40)  # RBLgpt logo
            with col2:
                st.markdown(msg["content"])

# ---------- Chat Input ----------
prompt = st.chat_input("Start typing your question...")
if prompt:
    question = prompt.strip()
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Reset suggestion state
    st.session_state.awaiting_confirmation = False
    st.session_state.suggested_q = ""
    st.session_state.suggested_ans = ""
    st.session_state.suggested_cat = ""

    # Check exact match in selected category
    match_row = selected_df[selected_df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        st.session_state.chat_history.append({"role": "assistant", "content": f"**Answer:** {answer}"})
    else:
        # No exact match → try suggestions
        all_questions = df["Question"].tolist()

        # Find best global and local matches
        best_global_match = get_close_matches(question, all_questions, n=1, cutoff=0.6)
        best_local_match = get_close_matches(question, selected_df["Question"].tolist(), n=1, cutoff=0.6)

        # Guess correct category from global match
        guessed_category = None
        if best_global_match:
            guessed_category = df[df["Question"] == best_global_match[0]].iloc[0]["Category"]

        # Prepare response
        response_text = ""
        if guessed_category and guessed_category != category:
            response_text += f"🗂 Your question might belong to **{guessed_category}** category.\n\n"

        if best_local_match:
            local_q = best_local_match[0]
            local_ans = selected_df[selected_df["Question"] == local_q].iloc[0]["Answer"]
            st.session_state.suggested_q = local_q
            st.session_state.suggested_ans = local_ans
            st.session_state.suggested_cat = category
            response_text += f"🤔 Did you mean (in this category): **{local_q}**?"
            st.session_state.awaiting_confirmation = True
        elif best_global_match:
            global_q = best_global_match[0]
            global_ans = df[df["Question"] == global_q].iloc[0]["Answer"]
            st.session_state.suggested_q = global_q
            st.session_state.suggested_ans = global_ans
            st.session_state.suggested_cat = guessed_category
            response_text += f"🤔 Did you mean: **{global_q}**? (_Category: {guessed_category}_)"
            st.session_state.awaiting_confirmation = True
        else:
            response_text = "I couldn't find a close match. Please try rephrasing."

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

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
    st.download_button(
        "📥 Download Chat",
        data=chat_text.encode("utf-8"),  # Convert to bytes
        file_name="chat_history.txt",
        mime="text/plain"
    )

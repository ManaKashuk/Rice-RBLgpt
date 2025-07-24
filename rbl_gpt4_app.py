import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image

# ---------- Config ----------
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
st.write("### Conversation")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='background:#e6f7ff;padding:10px;border-radius:8px;margin:5px 0;text-align:right;'>"
            f"<b>You:</b> {msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='display:flex;align-items:flex-start;margin:5px 0;'>
                <img src='data:image/png;base64,{logo.tobytes().hex()}' width='40' style='margin-right:10px;' />
                <div style='background:#f6f6f6;padding:10px;border-radius:8px;flex:1;'>
                    {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

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
        st.session_state.chat_history.append({"role": "assistant", "content": f"Answer: {answer}"})
    else:
        # Try to find closest matches
        all_questions = df["Question"].tolist()
        best_global_match = get_close_matches(question, all_questions, n=1, cutoff=0.6)
        best_local_match = get_close_matches(question, selected_df["Question"].tolist(), n=1, cutoff=0.6)

        response_text = ""
        if best_global_match:
            global_q = best_global_match[0]
            guessed_category = df[df["Question"] == global_q].iloc[0]["Category"]
            global_ans = df[df["Question"] == global_q].iloc[0]["Answer"]

            response_text += f"The question you asked seems to belong to the '{guessed_category}' category.\n\n"
            response_text += f"A similar question in that category is:\n{global_q}\n\n"
            response_text += "Would you like to see the answer?"

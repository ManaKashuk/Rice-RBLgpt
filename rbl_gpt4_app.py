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
if "suggested_list" not in st.session_state:
    st.session_state.suggested_list = []  # Store multiple suggestions

# ---------- Step 1: Category Selection ----------
category = st.selectbox("📂 Select a category:", ["All Categories"] + sorted(df["Category"].unique()))
selected_df = df if category == "All Categories" else df[df["Category"] == category]

# ---------- Display Chat ----------
st.write("### Conversation")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div style='background:#e6f7ff;padding:10px;border-radius:8px;margin:5px 0;text-align:right;'>"
                    f"<b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='display:flex;align-items:flex-start;margin:5px 0;'>
            <img src='data:image/png;base64,{logo.tobytes().hex()}' width='40' style='margin-right:10px;' />
            <div style='background:#f6f6f6;padding:10px;border-radius:8px;flex:1;'>
                {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------- Step 2: Chat Input with Autocomplete ----------
question = st.text_input("Start typing your question...", value="")

# Autocomplete suggestions (from selected category)
if question.strip():
    suggestions = [q for q in selected_df["Question"].tolist() if question.lower() in q.lower()][:5]
    if suggestions:
        st.markdown("**Suggestions:**")
        for s in suggestions:
            if st.button(s, key=f"suggest_{s}"):
                question = s  # Autofill
                st.session_state.chat_history.append({"role": "user", "content": question})

                # Direct answer
                ans = selected_df[selected_df["Question"] == s].iloc[0]["Answer"]
                st.session_state.chat_history.append({"role": "assistant", "content": f"Answer: {ans}"})
                st.rerun()

# Submit button for custom question
if st.button("Submit") and question.strip():
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Reset previous suggestions
    st.session_state.suggested_list = []

    # Check exact match in selected category
    match_row = selected_df[selected_df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        st.session_state.chat_history.append({"role": "assistant", "content": f"Answer: {answer}"})
    else:
        # If no exact match → Find top 3 suggestions globally
        all_questions = df["Question"].tolist()
        top_matches = get_close_matches(question, all_questions, n=3, cutoff=0.5)

        if top_matches:
            guessed_category = df[df["Question"] == top_matches[0]].iloc[0]["Category"]

            response_text = f"The question you asked seems to belong to the '{guessed_category}' category.\n\n"
            response_text += "Here are some similar questions:\n"
            for i, q in enumerate(top_matches, start=1):
                response_text += f"{i}. {q}\n"

            response_text += "\nClick a button below to see an answer."
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

            # Store these matches
            st.session_state.suggested_list = top_matches
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": "I couldn't find a close match. Please try rephrasing."})

    st.rerun()

# ---------- Step 3: Show Buttons for Top Suggestions ----------
if st.session_state.suggested_list:
    st.write("### Which question do you want the answer for?")
    for i, q in enumerate(st.session_state.suggested_list):
        if st.button(q, key=f"choice_{i}"):
            ans = df[df["Question"] == q].iloc[0]["Answer"]
            st.session_state.chat_history.append({"role": "assistant", "content": f"Answer: {ans}"})
            st.session_state.suggested_list = []  # Clear suggestions
            st.rerun()

# ---------- Download Chat ----------
if st.session_state.chat_history:
    chat_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history])
    st.download_button(
        "📥 Download Chat",
        data=chat_text.encode("utf-8"),
        file_name="chat_history.txt",
        mime="text/plain"
    )

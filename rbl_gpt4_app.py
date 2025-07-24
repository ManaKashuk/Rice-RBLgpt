import streamlit as st
import pandas as pd
from difflib import SequenceMatcher, get_close_matches
from PIL import Image
import base64
from io import BytesIO
import random

# ---------- Helper: Convert Logo to Base64 ----------
def get_image_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# ---------- Config & Logo ----------
st.set_page_config(page_title="Rice RBLPgpt", layout="centered")
logo = Image.open("RBLgpt logo.png")
logo_base64 = get_image_base64(logo)

st.markdown(
    f"""
    <div style='text-align:left;'>
        <img src='data:image/png;base64,{logo_base64}' width='100'/>
        <h2>Rice RBLPgpt</h2>
        <p2><i>Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</i></p2>
        <p>🧠 Trained to respond like a Rice Biotech LaunchPad Research Admin based on SOP guidance.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- Load CSV ----------
df = pd.read_csv("sample_questions.csv")

# ---------- Session State ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "suggested_list" not in st.session_state:
    st.session_state.suggested_list = []
if "last_category" not in st.session_state:
    st.session_state.last_category = ""
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# ---------- Category Selection ----------
category = st.selectbox("📂 Select a category:", ["All Categories"] + sorted(df["Category"].unique()))

# Reset session if category changes
if st.session_state.last_category != category:
    st.session_state.chat_history = []
    st.session_state.suggested_list = []
    st.session_state.last_category = category
    st.experimental_rerun()

selected_df = df if category == "All Categories" else df[df["Category"] == category]

# ---------- Display Chat ----------
st.markdown("<div style='margin-top:20px;'>", unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style='text-align:right;margin:10px 0;'>
                <div style='display:inline-block;background:#e6f7ff;padding:12px;border-radius:12px;max-width:70%;'>
                    <b>You:</b> {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='display:flex;align-items:flex-start;margin:10px 0;'>
                <img src='data:image/png;base64,{logo_base64}' width='40' style='margin-right:10px;border-radius:8px;'/>
                <div style='background:#f6f6f6;padding:12px;border-radius:12px;max-width:75%;'>
                    {msg['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- Chat Input ----------
question = st.text_input("💬 Start typing your question...", value="" if st.session_state.clear_input else "")
st.session_state.clear_input = False  # Reset after clearing

# Autocomplete suggestions
if question.strip():
    suggestions = [q for q in selected_df["Question"].tolist() if question.lower() in q.lower()][:5]
    if suggestions:
        st.markdown("<div style='margin-top:5px;'><b>Suggestions:</b></div>", unsafe_allow_html=True)
        for s in suggestions:
            if st.button(s, key=f"suggest_{s}"):
                st.session_state.chat_history.append({"role": "user", "content": s})
                ans = selected_df[selected_df["Question"] == s].iloc[0]["Answer"]
                st.session_state.chat_history.append({"role": "assistant", "content": f"<b>Answer:</b> {ans}"})
                st.session_state.clear_input = True
                st.rerun()

# ---------- Submit Question ----------
if st.button("Submit") and question.strip():
    st.session_state.chat_history.append({"role": "user", "content": question})

    previous_suggestions = st.session_state.suggested_list
    st.session_state.suggested_list = []
    st.session_state.clear_input = True  # Clear input after submit

    # Check for exact or close match
    all_questions = df["Question"].tolist()
    best_match = None
    best_score = 0
    for q in all_questions:
        score = SequenceMatcher(None, question.lower(), q.lower()).ratio()
        if score > best_score:
            best_match = q
            best_score = score

    if best_score >= 0.85:  # Only answer if confidence is high
        ans = df[df["Question"] == best_match].iloc[0]["Answer"]
        category_note = df[df["Question"] == best_match].iloc[0]["Category"]
        response_text = f"<b>Answer:</b> {ans}<br><i>(Note: This question belongs to the '{category_note}' category.)</i>"
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
    else:
        if previous_suggestions:
            # User ignored suggestions previously → show best global match
            ans = df[df["Question"] == previous_suggestions[0]].iloc[0]["Answer"]
            category_note = df[df["Question"] == previous_suggestions[0]].iloc[0]["Category"]
            response_text = f"<b>Answer:</b> {ans}<br><i>(Note: This question belongs to the '{category_note}' category.)</i>"
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        else:
            # Suggest top 3 questions instead of giving a wrong answer
            top_matches = get_close_matches(question, all_questions, n=3, cutoff=0.4)
            if top_matches:
                guessed_category = df[df["Question"] == top_matches[0]].iloc[0]["Category"]
                response_text = f"I couldn't find an exact match, but your question seems related to <b>{guessed_category}</b>.<br><br>"
                response_text += "Here are some similar questions:<br>"
                for i, q in enumerate(top_matches, start=1):
                    response_text += f"{i}. {q}<br>"
                response_text += "<br>Select one below to see its answer."
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                st.session_state.suggested_list = top_matches
            else:
                st.session_state.chat_history.append({"role": "assistant", "content": "I couldn't find a close match. Please try rephrasing."})

    st.rerun()

# ---------- Show Buttons for Top Suggestions ----------
if st.session_state.suggested_list:
    st.markdown("<div style='margin-top:15px;'><b>Choose a question:</b></div>", unsafe_allow_html=True)
    for i, q in enumerate(st.session_state.suggested_list):
        if st.button(q, key=f"choice_{i}"):
            ans = df[df["Question"] == q].iloc[0]["Answer"]
            st.session_state.chat_history.append({"role": "assistant", "content": f"<b>Answer:</b> {ans}"})
            st.session_state.suggested_list = []
            st.session_state.clear_input = True
            st.rerun()

# ---------- Show Related Questions After Every Answer ----------
if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "assistant" and not st.session_state.suggested_list:
    if len(selected_df) > 3:
        related_questions = random.sample(selected_df["Question"].tolist(), 3)
        st.markdown("<div style='margin-top:15px;'><b>Want to continue? Try these:</b></div>", unsafe_allow_html=True)
        for rq in related_questions:
            if st.button(rq, key=f"related_{rq}"):
                st.session_state.chat_history.append({"role": "user", "content": rq})
                ans = selected_df[selected_df["Question"] == rq].iloc[0]["Answer"]
                st.session_state.chat_history.append({"role": "assistant", "content": f"<b>Answer:</b> {ans}"})
                st.session_state.clear_input = True
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

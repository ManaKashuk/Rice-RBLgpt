import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image
import base64
from io import BytesIO

# ---------- Helper: Convert Logo to Base64 ----------
def get_image_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# ---------- Config & Logo ----------
st.set_page_config(page_title="Rice RBLgpt", layout="centered")
logo = Image.open("RBLgpt logo.png")
logo_base64 = get_image_base64(logo)

st.markdown(
    f"""
    <div style='text-align:center;'>
        <img src='data:image/png;base64,{logo_base64}' width='100'/>
        <h2>Rice RBLgpt</h2>
        <p><i>Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</i></p>
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

# ---------- Category Selection ----------
category = st.selectbox("📂 Select a category:", ["All Categories"] + sorted(df["Category"].unique()))
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

# ---------- Chat Input with Autocomplete ----------
question = st.text_input("💬 Start typing your question...")
if question.strip():
    # Show autocomplete suggestions
    suggestions = [q for q in selected_df["Question"].tolist() if question.lower() in q.lower()][:5]
    if suggestions:
        st.markdown("<div style='margin-top:5px;'><b>Suggestions:</b></div>", unsafe_allow_html=True)
        for s in suggestions:
            if st.button(s, key=f"suggest_{s}"):
                question = s
                st.session_state.chat_history.append({"role": "user", "content": question})
                ans = selected_df[selected_df["Question"] == s].iloc[0]["Answer"]
                st.session_state.chat_history.append({"role": "assistant", "content": f"<b>Answer:</b> {ans}"})
                st.rerun()

# ---------- Submit Question ----------
if st.button("Submit") and question.strip():
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Reset old suggestions
    st.session_state.suggested_list = []

    # Check for exact match in selected category
    match_row = selected_df[selected_df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        st.session_state.chat_history.append({"role": "assistant", "content": f"<b>Answer:</b> {answer}"})
    else:
        # No exact match → find top 3 suggestions from all questions
        all_questions = df["Question"].tolist()
        top_matches = get_close_matches(question, all_questions, n=3, cutoff=0.4)

        if top_matches:
            guessed_category = df[df["Question"] == top_matches[0]].iloc[0]["Category"]
            response_text = f"The question you asked seems to belong to the <b>{guessed_category}</b> category.<br><br>"
            response_text += "Here are some similar questions:<br>"
            for i, q in enumerate(top_matches, start=1):
                response_text += f"{i}. {q}<br>"
            response_text += "<br>Select a question below to see its answer."
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

            # Save suggestions for buttons
            st.session_state.suggested_list = top_matches
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": "I couldn't find a close match. Please try rephrasing."})

    st.rerun()

# ---------- Show Buttons for Suggestions ----------
if st.session_state.suggested_list:
    st.markdown("<div style='margin-top:15px;'><b>Choose a question:</b></div>", unsafe_allow_html=True)
    for i, q in enumerate(st.session_state.suggested_list):
        if st.button(q, key=f"choice_{i}"):
            ans = df[df["Question"] == q].iloc[0]["Answer"]
            st.session_state.chat_history.append({"role": "assistant", "content": f"<b>Answer:</b> {ans}"})
            st.session_state.suggested_list = []
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

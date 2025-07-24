import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image
import base64
from io import BytesIO

# ---------- Helper: Convert logo to base64 ----------
def get_base64_logo(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ---------- Config ----------
st.set_page_config(page_title="Rice RBLPgpt", layout="centered")
logo = Image.open("RBLgpt logo.png")
logo_base64 = get_base64_logo(logo)

st.image(logo, width=100)
st.markdown("<h2 style='text-align: left; margin-top: -20px;'>Rice RBLgpt</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; margin-top: -10px;'>Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad</h5>", unsafe_allow_html=True)
st.markdown("🧠 _Trained to respond like a Rice Biotech LaunchPad Research Admin based on SOP guidance._")

# ---------- File Upload ----------
uploaded_file = st.file_uploader("📎 Upload a file (PDF, CSV, etc.)", type=["pdf", "csv", "txt"])
if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    if uploaded_file.type == "text/csv":
        df_uploaded = pd.read_csv(uploaded_file)
        st.dataframe(df_uploaded.head())
    elif uploaded_file.type == "text/plain":
        st.text(uploaded_file.read().decode("utf-8")[:500])
    elif uploaded_file.type == "application/pdf":
        st.info("PDF uploaded. (Parsing not yet implemented)")

# ---------- Load CSV ----------
df = pd.read_csv("sample_questions.csv")

# ---------- Session State Initialization ----------
for key, default in {
    "chat_history": [],
    "awaiting_confirmation": False,
    "suggested_q": "",
    "suggested_ans": "",
    "suggested_cat": "",
    "typed_question": "",
    "messages": [],
    "prev_category": "All Categories"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------- Category Selection ----------
category = st.selectbox("📂 Select a category:", ["All Categories"] + sorted(df["Category"].unique()))

# Reset typed_question if category changed
if category != st.session_state.prev_category:
    st.session_state.typed_question = ""
    st.session_state.prev_category = category

selected_df = df if category == "All Categories" else df[df["Category"] == category]

# ---------- Suggested Questions (Top 3 Buttons) ----------
if not st.session_state.typed_question:
    st.markdown("💬 Try asking:")
    examples = selected_df["Question"].head(3).tolist()
    for i, example in enumerate(examples):
        if st.button(example, key=f"try_btn_{i}"):
            answer = selected_df[selected_df["Question"] == example]["Answer"].values[0]
            st.session_state.chat_history.append({"role": "user", "content": example})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.session_state.typed_question = example
            st.rerun()

# ---------- Display Chat History ----------
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style='background:#e6f7ff;padding:10px;border-radius:8px;margin:5px 0;text-align:right;'>
                    <b>You:</b> {msg['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='display:flex;align-items:center;margin:5px 0;'>
                    <img src='data:image/png;base64,{logo_base64}' width='40' style='margin-right:10px;' />
                    <div style='background:#f6f6f6;padding:10px;border-radius:8px;flex:1;'>
                        {msg['content']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ---------- Chat Input ----------
st.markdown("<div style='margin-top:-10px;'></div>", unsafe_allow_html=True)  # Reduce spacing
prompt = st.chat_input("Start typing your question...")
if prompt:
    question = prompt.strip()
    st.session_state.typed_question = question
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Reset suggestion state
    for key in ["awaiting_confirmation", "suggested_q", "suggested_ans", "suggested_cat"]:
        st.session_state[key] = False if key == "awaiting_confirmation" else ""

    # Search logic
    match_row = selected_df[selected_df["Question"].str.lower() == question.lower()]
    if not match_row.empty:
        answer = match_row.iloc[0]["Answer"]
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        all_questions = df["Question"].tolist()
        best_global_match = get_close_matches(question, all_questions, n=1, cutoff=0.6)
        best_local_match = get_close_matches(question, selected_df["Question"].tolist(), n=1, cutoff=0.6)

        guessed_category = None
        response_text = ""

        if best_global_match:
            guessed_category = df[df["Question"] == best_global_match[0]].iloc[0]["Category"]

        if best_local_match:
            local_q = best_local_match[0]
            local_ans = selected_df[selected_df["Question"] == local_q].iloc[0]["Answer"]
            st.session_state.suggested_q = local_q
            st.session_state.suggested_ans = local_ans
            st.session_state.suggested_cat = category
            response_text += f"🤔 Did you mean: {local_q}?"
            st.session_state.awaiting_confirmation = True
        elif best_global_match:
            global_q = best_global_match[0]
            global_ans = df[df["Question"] == global_q].iloc[0]["Answer"]
            st.session_state.suggested_q = global_q
            st.session_state.suggested_ans = global_ans
            st.session_state.suggested_cat = guessed_category
            response_text += f"🤔 Did you mean: {global_q}? [Category: {guessed_category}]"
            st.session_state.awaiting_confirmation = True

        else:
            # Keyword-based fallback
            keyword_matches = [q for q in all_questions if any(word in q.lower() for word in question.lower().split())]
            if keyword_matches:
                best_keyword_match = keyword_matches[0]
                keyword_category = df[df["Question"] == best_keyword_match].iloc[0]["Category"]
                keyword_answer = df[df["Question"] == best_keyword_match].iloc[0]["Answer"]
        
                st.session_state.suggested_q = best_keyword_match
                st.session_state.suggested_ans = keyword_answer
                st.session_state.suggested_cat = keyword_category
                response_text = f"🤔 Did you mean: **{best_keyword_match}**? (_Category: {keyword_category}_)"
                st.session_state.awaiting_confirmation = True
            else:
                response_text = "Sorry, I couldn’t find a close match. Please try rephrasing or selecting a category."
        
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

    st.rerun()

# ---------- Suggestion Confirmation Buttons ----------
if st.session_state.awaiting_confirmation:
    st.write("### Choose an option:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, show answer"):
            st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.suggested_ans})
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
        data=chat_text.encode("utf-8"),
        file_name="chat_history.txt",
        mime="text/plain"
    )

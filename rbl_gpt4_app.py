import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image

# ---------- Config & Logo ----------
st.set_page_config(page_title="Rice RBLgpt", layout="centered")

logo = Image.open("RBLgpt_logo.png")
st.image(logo, width=100)
st.markdown("<h2>Rice RBLgpt</h2>", unsafe_allow_html=True)
st.markdown("_Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad_")
st.markdown("🧠 _RBLgpt is trained to respond like a Rice research admin based on SOP guidance._")

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

# ---------- Step 2: Ask a Question ----------
# Show autocomplete dropdown as suggestions
st.markdown("💬 **Type your question** (or select from suggestions):")

selected_suggestion = st.selectbox(
    "Suggestions:", [""] + category_questions, key="dropdown_suggest"
)

if selected_suggestion:
    st.session_state.typed_question = selected_suggestion
    st.experimental_rerun()

# Input box for custom question
question = st.text_input("Your question:", value=st.session_state.typed_question)
submit = st.button("Submit")

# ---------- Step 3: Process the Question ----------
if submit and question.strip():
    question = question.strip()
    st.session_state.typed_question = ""  # Clear for next round

    # Show user's message
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

    # If no exact match, try close match from ALL categories
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

# ---------- Step 6: Show Chat History ----------
st.divider()
st.markdown("💻 **Chat History**")
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            col1, col2 = st.columns([1, 10])
            with col1:
                st.image(logo, width=40)
            with col2:
                st.markdown(f"**Answer:** {msg['content']}")


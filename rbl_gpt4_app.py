import streamlit as st
import pandas as pd
from difflib import get_close_matches
from PIL import Image
import io

# --- CONFIG ---
st.set_page_config("RBLgpt", layout="centered")

# --- LOGO + TITLE ---
logo = Image.open("RBLgpt logo.png")
st.image(logo, width=90)
st.markdown("## Rice RBLgpt")
st.markdown("_Smart Assistant for Rice Biotech LaunchPad_")

# --- Load CSV ---
df = pd.read_csv("sample_questions.csv")

# --- SESSION STATE INIT ---
if "chat" not in st.session_state:
    st.session_state.chat = []  # stores all {"role": "user"/"assistant", "content": str}
if "suggested" not in st.session_state:
    st.session_state.suggested = None  # stores a suggestion dict if needed

# --- DISPLAY CHAT ---
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- HANDLE SUGGESTION RESPONSE ---
if st.session_state.suggested:
    with st.chat_message("assistant"):
        st.markdown(f"🤔 Did you mean:\n**{st.session_state.suggested['q']}**\n\n_Category: {st.session_state.suggested['cat']}_")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, show answer"):
                st.session_state.chat.append({"role": "assistant", "content": st.session_state.suggested["ans"]})
                st.session_state.suggested = None
                st.rerun()
        with col2:
            if st.button("❌ No, ask again"):
                st.session_state.suggested = None
                st.rerun()

# --- MAIN CHAT INPUT ---
if not st.session_state.suggested:
    prompt = st.chat_input("Start typing...")
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})

        # Search CSV
        exact_match = df[df["Question"].str.lower() == prompt.lower()]
        if not exact_match.empty:
            answer = exact_match.iloc[0]["Answer"]
            st.session_state.chat.append({"role": "assistant", "content": answer})
            st.rerun()
        else:
            # Try fuzzy match
            all_qs = df["Question"].tolist()
            matches = get_close_matches(prompt, all_qs, n=1, cutoff=0.5)
            if matches:
                best = matches[0]
                row = df[df["Question"] == best].iloc[0]
                st.session_state.suggested = {
                    "q": best,
                    "ans": row["Answer"],
                    "cat": row["Category"]
                }
                st.rerun()

# --- DOWNLOAD CHAT HISTORY ---
if st.session_state.chat:
    lines = [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat]
    download_text = "\n\n".join(lines)
    buffer = io.StringIO(download_text)
    st.download_button("📥 Download Chat", buffer, file_name="chat_history.txt", mime="text/plain")

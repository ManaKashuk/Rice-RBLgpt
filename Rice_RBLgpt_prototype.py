
import streamlit as st

st.set_page_config(page_title="Rice RBLgpt | Smart Assistant for Research Admin", layout="wide")

st.title("📘 Rice RBLgpt")
st.subheader("Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad")

# Sidebar Navigation
section = st.sidebar.selectbox("Select a workflow area:", ["Pre-Award", "Post-Award"])

# Prompt examples
examples = {
    "Pre-Award": [
        "What internal documents are needed before submitting a Cayuse proposal at Rice?",
        "How do I route for Chair/Dean approval?",
        "How do I initiate a Cayuse submission for NIH?"
    ],
    "Post-Award": [
        "Where can I see budget burn rate for my award?",
        "How do I request a no-cost extension in iO?",
        "What are the steps to re-budget in post-award phase?"
    ]
}

st.markdown("### Ask Rice RBLgpt a question:")
user_input = st.text_input("🔍 Question")

if user_input:
    with st.spinner("Thinking..."):
        st.markdown("**💬 Answer:**")
        st.success(f"Simulated RBLgpt response for the '{section}' workflow. You asked: '{user_input}'")

# Show prompt examples
st.markdown("### 🧠 Example Questions")
for example in examples[section]:
    st.markdown(f"- {example}")

st.sidebar.markdown("---")
st.sidebar.markdown("Prototype by Mana | HDHC @ Rice | Inspired by Emory ORA-GPT")

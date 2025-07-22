
import streamlit as st

st.set_page_config(page_title="Rice RBLgpt", page_icon="🧠", layout="wide")

# Display the Rice RBL logo
st.image("https://images.squarespace-cdn.com/content/v1/64e3b8652d51484e88798b28/d6b0de0c-44c7-4796-a116-2ab6da4f7bb0/BiotechLaunchPad.png?format=1500w", width=300)

# App title and subtitle
st.title("📘 Rice RBLgpt")
st.subheader("Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad")

# Sidebar selection
workflow = st.sidebar.radio("Choose Workflow Area:", ("Pre-Award", "Post-Award"))

# Input field
user_input = st.text_input("🔍 Ask Rice RBLgpt a question:")

# Simulated answer logic
if user_input:
    st.markdown(f"💬 **Answer:**\n\nSimulated RBLgpt response for the **{workflow}** workflow.\n\nYou asked: '{user_input}'")

# Sample prompts
st.markdown("🧠 **Example Questions**")
if workflow == "Pre-Award":
    st.markdown("""
    - What internal documents are needed before submitting a Cayuse proposal at Rice?
    - How do I route for Chair/Dean approval?
    - How do I initiate a Cayuse submission for NIH?
    """)
else:
    st.markdown("""
    - Where can I see budget burn rate for my award?
    - How do I request a no-cost extension in iO?
    - What’s the process to submit an expenditure justification?
    """)


import streamlit as st

# Set page config
st.set_page_config(page_title="Rice RBLgpt", layout="wide")

# Display the banner image
st.image("https://drive.google.com/uc?export=view&id=19bb1cBQ5JBY-ntN0E5vqI3pQZ9pmSvpJ", use_column_width=True)

# Title and subtitle
st.title("Rice RBLgpt")
st.subheader("Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad")

# Sidebar
st.sidebar.title("Workflow Type")
workflow = st.sidebar.radio("Choose a workflow:", ["Pre-Award", "Post-Award"])

# Example questions
example_questions = {
    "Pre-Award": [
        "What internal documents are needed before submitting a Cayuse proposal at Rice?",
        "How do I route for Chair/Dean approval?",
        "How do I initiate a Cayuse submission for NIH?"
    ],
    "Post-Award": [
        "Where can I see budget burn rate for my award?",
        "How do I request a no-cost extension in iO?",
        "What expenses are allowable under federal grants?"
    ]
}

# Input section
question = st.text_input("Ask Rice RBLgpt a question:")

# Simulated response
if question:
    st.write("💬 Answer:")
    st.info(f"Simulated RBLgpt response for the '{workflow}' workflow. You asked: '{question}'")

# Display example questions
st.markdown("### 🧠 Example Questions")
for q in example_questions[workflow]:
    st.markdown(f"- {q}")

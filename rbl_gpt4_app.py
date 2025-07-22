
import streamlit as st

# Display the Rice Biotech LaunchPad logo
st.image(
    "https://images.squarespace-cdn.com/content/v1/64e3b8652d51484e88798b28/d6b0de0c-44c7-4796-a116-2ab6da4f7bb0/BiotechLaunchPad.png?format=1500w",
    width=300
)

st.title("Rice RBLgpt")
st.subheader("Smart Assistant for Pre- & Post-Award Support at Rice Biotech LaunchPad")

question = st.text_input("Ask Rice RBLgpt a question:")

if question:
    if "Chair" in question or "Dean" in question:
        response = "To route for Chair/Dean approval, log into Cayuse, complete the internal proposal routing form, and select your department for review. The system will notify the Chair/Dean automatically."
    elif "Cayuse" in question:
        response = "Before submitting a Cayuse proposal, you’ll need a PI certification form, budget justification, and internal routing approvals."
    elif "no-cost extension" in question or "iO" in question:
        response = "To request a no-cost extension in iO, initiate the request via the iO Grant Management dashboard and attach a justification letter. Contact your grant manager for final submission."
    else:
        response = f"Simulated RBLgpt response for the workflow. You asked: '{question}'"

    st.write("💬 **Answer:**")
    st.info(response)

st.markdown("### 🧠 Example Questions")
st.markdown("""
- What internal documents are needed before submitting a Cayuse proposal at Rice?
- How do I route for Chair/Dean approval?
- How do I request a no-cost extension in iO?
""")

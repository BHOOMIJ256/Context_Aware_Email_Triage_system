import streamlit as st
import requests

st.set_page_config(page_title="Live Email Triage", layout="centered")
st.title("📩 Live Email Triage System")

st.markdown("Paste an email below to analyze its **category**, **tone**, **urgency**, and get a **suggested reply**.")

email = st.text_area("✉️ Email Content", height=200)

if st.button("Analyze Email"):
    if email.strip() == "":
        st.warning("Please enter a valid email text.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/triage",  # Update if hosted elsewhere
                    json={"email": email}
                )
                result = response.json()

                st.success("✅ Analysis Complete")

                st.markdown("### 🧠 AI Analysis Result")
                st.write(f"**Category:** {result['category']}")
                st.write(f"**Tone:** {result['tone']}")
                st.write(f"**Urgency:** {result['urgency']}")
                st.write("**Suggested Reply:**")
                st.code(result['suggested_reply'], language="markdown")

                st.write(f"**Attachment Detected?** {'📎 Yes' if result['has_attachment'] else '❌ No'}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

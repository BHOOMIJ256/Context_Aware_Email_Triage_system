# send_email_page.py

import streamlit as st
import pandas as pd
import sqlite3
from Send_Mail import send_email  # ✅ Your existing email sender
import os

st.title("📤 Send Email to User")

# 🔹 Step 1: Connect to your SQLite DB and fetch triaged emails
db_path = os.path.join(os.path.dirname(__file__), '..', 'emails.db')
conn = sqlite3.connect(db_path)
query = "SELECT created_at, category, tone, urgency, email, sender_email FROM triage_results ORDER BY created_at DESC LIMIT 10"
df = pd.read_sql_query(query, conn)
conn.close()

# 🔹 Step 2: UI to select a triaged email
st.subheader("📬 Select a triaged email to respond to:")
selected_email = st.selectbox("Select an email:", df['email'])

if selected_email:
    row = df[df['email'] == selected_email].iloc[0]
    recipient = row['sender_email']
    default_subject = f"RE: {row['category']} - Regarding your email"

    subject_input = st.text_input("Subject", value=default_subject)
    reply_message = st.text_area("Your message")

    # 🔹 Step 3: Send email on button click
    if st.button("📤 Send Email"):
        if recipient and reply_message.strip():
            success = send_email(recipient, subject_input, reply_message)
            if success:
                st.success("✅ Email sent successfully!")
            else:
                st.error("❌ Failed to send email.")
        else:
            st.warning("Recipient or message is missing.")

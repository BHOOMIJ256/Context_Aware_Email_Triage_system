import sqlite3
import pandas as pd
from datetime import datetime
from Send_Mail import send_email  # Make sure it's in the root or adjust import path

# Step 1: Load latest data
def load_data():
    conn = sqlite3.connect("emails.db")
    df = pd.read_sql_query("SELECT * FROM triage_results", conn)
    conn.close()
    return df

# Step 2: Prepare summary
def generate_summary(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['urgency'] = df['urgency'].str.strip().str.title()
    df['category'] = df['category'].str.strip().str.title()

    # Top 5 high urgency emails (most recent)
    top_urgent = df[df['urgency'] == 'High'].sort_values(by='created_at', ascending=False).head(5)

    # Most frequent category
    top_category = df['category'].value_counts().idxmax()
    top_category_count = df['category'].value_counts().max()

    # Format email body
    body = f"📬 **Daily Triage Summary - {datetime.now().strftime('%B %d, %Y')}**\n\n"

    body += "🛑 **Top 5 High-Urgency Emails:**\n"
    for i, row in top_urgent.iterrows():
        body += f"\n• [{row['created_at']}] {row['category']} | {row['tone']} | {row['email'][:80]}...\n"

    body += f"\n📊 **Top Category Today:** {top_category} ({top_category_count} emails)\n"

    return body

# Step 3: Send the email
def send_daily_summary():
    df = load_data()
    if df.empty:
        print("No data to send.")
        return

    body = generate_summary(df)
    subject = "📬 Daily Email Triage Summary"

    # Set this to your or team's email
    to_address = "bhoomi901jain@gmail.com"

    send_email(to_address=to_address, subject=subject, body=body)
    print("✅ Daily summary email sent.")

# Run this if script is triggered
if __name__ == "__main__":
    send_daily_summary()

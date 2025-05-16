import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Email Sentiment Dashboard", layout="wide")

st_autorefresh(interval=10000, limit=None, key="dashboard_refresh")

st.title("📊 Sentiment Trend Dashboard")


# Load data from SQLite
@st.cache_data(ttl=5)
def load_data():
    conn = sqlite3.connect("emails.db")
    df = pd.read_sql_query("SELECT * FROM triage_results ORDER BY created_at DESC", conn)
    conn.close()
    return df

# Load data
df = load_data()



# Summary metrics using columns
st.markdown("### Dashboard Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📬 Total Emails", len(df))

with col2:
    st.metric("📂 Unique Categories", df['category'].nunique())

with col3:
    st.metric("⚠️ High Urgency Emails", df[df['urgency'].str.lower().str.strip() == 'high'].shape[0])

df['urgency'] = df['urgency'].str.strip().str.title()
df['category'] = df['category'].str.strip().str.title()
df['tone'] = df['tone'].str.strip().str.capitalize()


if df.empty:
    st.warning("No data available yet. Submit some emails via the /triage endpoint.")
    st.stop()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    

    # Normalize values: strip whitespace, title case (e.g., 'low' -> 'Low')
    df['category'] = df['category'].str.strip().str.title()
    df['tone'] = df['tone'].str.strip().str.title()
    df['urgency'] = df['urgency'].str.strip().str.title()

    unique_categories = sorted(df['category'].dropna().unique())
    unique_tones = sorted(df['tone'].dropna().unique())
    unique_urgencies = sorted(df['urgency'].dropna().unique())

    selected_category = st.multiselect("Filter by Category", unique_categories, default=unique_categories)
    selected_tone = st.multiselect("Filter by Tone", unique_tones, default=unique_tones)
    selected_urgency = st.multiselect("Filter by Urgency", unique_urgencies, default=unique_urgencies)

# Filtered data
filtered_df = df[
    (df['category'].isin(selected_category)) &
    (df['tone'].isin(selected_tone)) &
    (df['urgency'].isin(selected_urgency))
].sort_values(by="id", ascending=False)

# ✅ NEW: Toggle to apply filters to graphs
use_filtered = st.checkbox("📈 Apply Filters to Trend Charts", value=True)
trend_data = filtered_df if use_filtered else df

# Show recent emails
st.subheader("📬 Recent Triaged Emails")

# Display the first 5 emails directly
st.dataframe(filtered_df.head(5)[['created_at', 'category', 'tone', 'urgency', 'email']], use_container_width=True)

# Collapsible section for viewing all remaining emails
with st.expander("📜 View All Emails"):
    st.dataframe(filtered_df[['created_at', 'category', 'tone', 'urgency', 'email']], use_container_width=True, height=300)

# Trends over time
st.subheader("📈 Tone and Urgency Trends")

col1, col2 = st.columns(2)

with col1:
    tone_trend = (
        trend_data.groupby([pd.to_datetime(trend_data['created_at']).dt.date.rename('date'), 'tone'])
        .size().reset_index(name='count')
    )
    tone_chart = alt.Chart(tone_trend).mark_line(point=True).encode(
        x='date:T',
        y='count:Q',
        color='tone:N'
    ).properties(title="Tone Trend Over Time", width=500)
    st.altair_chart(tone_chart)

with col2:
    urgency_trend = (
        trend_data.groupby([pd.to_datetime(trend_data['created_at']).dt.date.rename('date'), 'urgency'])
        .size().reset_index(name='count')
    )
    urgency_chart = alt.Chart(urgency_trend).mark_bar().encode(
        x='date:T',
        y='count:Q',
        color='urgency:N'
    ).properties(title="Urgency Trend Over Time", width=500)
    st.altair_chart(urgency_chart)


   

# Feedback Editor Section
st.markdown("---")
st.subheader("✏️ Feedback Editor (Edit Suggested Replies)")

# Ensure 'id' and 'reply' columns exist
if 'id' not in filtered_df.columns or 'reply' not in filtered_df.columns:
    st.warning("The required 'id' or 'reply' fields are missing in the database.")
else:
    if not filtered_df.empty:
        selected_email_id = st.selectbox("Select Email ID to Give Feedback", filtered_df['id'])

        email_row = filtered_df[filtered_df['id'] == selected_email_id].iloc[0]

        st.write("#### 📩 Email Content:")
        st.code(email_row['email'], language="markdown")

        st.write("#### 🤖 Suggested Reply (LLM):")
        st.code(email_row['reply'], language="markdown")

        st.write("#### ✍️ Your Edited Reply:")
        user_reply = st.text_area("Modify and save the reply below:", value=email_row.get('user_reply') or email_row['reply'], height=200)

        if st.button("💾 Save Edited Reply"):
            conn = sqlite3.connect("emails.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE triage_results SET user_reply = ?, feedback_timestamp = CURRENT_TIMESTAMP WHERE id = ?",
                (user_reply, selected_email_id)
            )
            conn.commit()
            conn.close()
            st.success("✅ Edited reply saved successfully.")
    else:
        st.info("No triaged emails to provide feedback on.")




<h1>🎯Problem Statment</h1>

Modern customer support, B2B sales, and operations teams receive hundreds to thousands of emails daily — inquiries, complaints, follow-ups, urgent escalations, and more.
**Manually reading, categorizing, and prioritizing each email causes:**

> **Delayed response time**s

> **Missed high-urgency messages**

> **Poor customer experience**

> **Inefficient team workflows**

As email volumes grow, enterprises need an **automated, intelligent triage system** that understands context, urgency, and sentiment to support faster and smarter decision-making.

# 💡Solution : Context Aware Email Triage System for Enterprise Teams
The Email Triage System is an intelligent pipeline for automating the classification, prioritization, sentiment detection, and visualization of incoming emails. It aims to reduce manual effort in sorting emails and support decision-making by providing timely insights through a live dashboard and daily email summaries.

<h1>✅ Core Functionalities</h1>

# 1. Email Triage API (/triage)

* Built using **FastAPI**.

* Accepts incoming emails via POST requests.

* **Processes each email** to extract:

   * **Tone/Sentiment** (e.g., Positive, Neutral, Negative).

   * **Urgency** (High, Medium, Low).

   * **Category** (e.g., Support, Feedback, Complaint) using custom or ML classification.

* Stores processed results in **SQLite (emails.db)**.

* Optional support for handling **attachments**, HTML parsing, and auto-responses.

# 2. Email Inbox Integration (IMAP)
* Automatically fetches emails from **Gmail/Outlook** using **IMAP**.

* **Parses and sends** them to the **/triage endpoint in real time**.

* Runs as a background service or cron job.

# 3. Database (emails.db)
* A SQLite database with table triage_results:
  
       id, email, tone, urgency, category, created_at    
              
* Stores triaged email data with timestamp.

* Keeps history for trend analysis and summaries.

# 4  Live Sentiment Dashboard (📊 Streamlit App)

Accessible via **Dashboard.py**

💡 Features:
* **Auto-refreshes** every 10 seconds (streamlit_autorefresh)

* **Displays**:

  * Total Emails

  * Unique Categories

  * High Urgency Emails

* **Filter Panel** (Category, Tone, Urgency)

* **Recent 5 Triaged Emails** (Sorted by most recent)

* **All Emails Viewer** (Collapsible section)

* **Apply Filters to Charts toggle**

* **Trends Over Time** (Using Altair Charts)

* **Fully dynamic** – updates in real-time as new emails arrive.

#  5. Email Sending Module (send_email.py)

* Handles sending email notifications.

* Used for sending daily summaries and could be extended for auto-replies.

* Works via smtplib or can be upgraded to SendGrid/Mailgun integration.

# 6. Daily Triage Summary Email

* Scheduled script (daily_summary.py):

  * Extracts top 5 high urgency emails of the day.

  * Detects the most frequent category.

  * Sends a summary email to the team using the send_email module.

* Can be automated using:

  * Windows Task Scheduler

  * Cron Jobs (Linux/macOS)

 #  🛠️ Tech Stack

| Component         | Technology              |
| ----------------- | ----------------------- |
| Backend API       | FastAPI                 |
| Database          | SQLite                  |
| Frontend          | Streamlit               |
| Visualization     | Altair + Pandas         |
| Email Sender      | smtplib                 |
| Inbox Fetching    | imaplib                 |
| Scheduler         | Cron/Task Scheduler     |

# ✅ Business Impact
⏱️ Reduces email response time by surfacing high-priority emails instantly

🤖 Automates repetitive tasks like email categorization and status tagging

📈 Enables performance tracking and team accountability through visual dashboards

💼 Scales easily for startups, support desks, and enterprise communication workflows

# Demo Video 

https://github.com/user-attachments/assets/1c67b7cb-e81e-49c3-acc8-188cf139f988






  

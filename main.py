from fastapi import FastAPI, Request
from utils.llm_handler import call_llm
from utils.cleaner import clean_email
from pathlib import Path
import sqlite3
import email
from email import policy

app = FastAPI()

def load_prompt(name):
    return Path(f"prompts/{name}").read_text()

@app.get("/")
def root():
    return {"message": "Email Triage System is running!"}


def clean_label(value):
    """Strip markdown formatting, get first word, and capitalize."""
    if value:
        return value.replace("*", "").split()[0].strip().capitalize()
    return "Unknown"

@app.post("/triage")
async def triage(request: Request):
    data = await request.json()
    email = clean_email(data["email"])
    has_attachment = detect_attachment(email)
    sender_email = data.get("sender_email","unknown@unknown.com" )

    # Step 1: Classify email
    prompt = load_prompt("classify.txt").replace("{{email}}", email)
    category = call_llm(prompt).strip()

    # Step 2: Tone & Urgency
    prompt = load_prompt("tone_urgency.txt").replace("{{email}}", email)
    tone_urgency = call_llm(prompt).strip()

    tone = "Unknown"
    urgency = "Unknown"
    try:
        parts = [line.split(":", 1)[1].strip() for line in tone_urgency.splitlines() if ":" in line]
        tone_raw = parts[0] if len(parts) > 0 else "Unknown"
        urgency_raw = parts[1] if len(parts) > 1 else "Unknown"

        # 🧼 Clean tone & urgency
        tone = clean_label(tone_raw)
        urgency = clean_label(urgency_raw)

    except Exception as e:
        print("⚠️ Tone/Urgency parsing failed:", e)

    # 🧼 Clean category as well (in case it includes LLM artifacts)
    category = clean_label(category)

    # Step 3: Generate response
    reply_prompt = load_prompt("generate_reply.txt")
    reply_prompt = (reply_prompt.replace("{{email}}", email)
                                  .replace("{{category}}", category)
                                  .replace("{{tone}}", tone)
                                  .replace("{{urgency}}", urgency))
    
    reply = call_llm(reply_prompt).strip()

    # Step 4: Save to db
    save_to_db(email, category, tone, urgency, reply, sender_email)

    return {
        "category": category,
        "tone": tone,
        "urgency": urgency,
        "suggested_reply": reply,
        "has_attachment": has_attachment
    }

def detect_attachment(email: str) -> bool:
    """Detects if common attachment types are mentioned in the email text."""
    keywords = [
        ".pdf", ".docx", ".xlsx", ".zip", ".xls", ".ppt", ".png", ".jpg", ".jpeg", ".txt",
        "pdf", "invoice", "attachment", "attached", "document", "file", "report"
    ]
    return any(word in email.lower() for word in keywords)

def save_to_db(email, category, tone, urgency, reply, sender_email):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute('''
       INSERT INTO triage_results (email, category, tone, urgency, reply, created_at, sender_email)
    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
    ''', (email, category, tone, urgency, reply, sender_email))
    conn.commit()
    conn.close()
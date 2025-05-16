import re

def clean_email(email: str) -> str:
    email = re.sub(r'\s+', ' ', email)
    return email.strip()

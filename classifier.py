from groq import Groq
import csv
import json
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key)
def classify_and_reply(subject, body, sender="unknown"):
    prompt = f"""You are an email triage assistant. Analyze this email and return ONLY a JSON object with these exact keys:
- "category": one of [urgent, follow_up, info, spam]
- "priority": integer 1-5 (5 = most urgent)
- "draft_reply": a professional 2-sentence reply
- "reason": one sentence explaining your classification

Email:
Subject: {subject}
From: {sender}
Body: {body}

Return ONLY valid JSON. No markdown, no extra text."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    result = json.loads(text.strip())
    result["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result["subject"] = subject
    result["sender"] = sender
    return result

def log_result(result):
    file_exists = os.path.isfile("log.csv")
    with open("log.csv", "a", newline="") as f:
        fieldnames = ["timestamp", "sender", "subject", "category", "priority", "reason", "draft_reply"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: result.get(k, "") for k in fieldnames})
    print(f"Logged: [{result['category'].upper()}] {result['subject']}")

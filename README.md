# AI Email Triage Bot

Automatically classifies emails by urgency and drafts replies using AI.

## Live Demo
https://email-triage-bot-lqpzcqnt544ts3a89wkcvy.streamlit.app/

## What it does
- Classifies emails: urgent / follow_up / info / spam
- Drafts a professional 2-sentence reply for each
- Logs all results to CSV
- Shows live metrics in a Streamlit dashboard

## ROI
- Build time: ~3 hours
- Saves: ~10 hrs/month of manual triage
- Cost: Free (Groq API free tier)

## Tech Stack
- Python, Streamlit, Groq API (llama-3.1-8b-instant)
- CSV logging, real-time dashboard

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install groq streamlit pandas python-dotenv
```

Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_key_here
```

## Run
```bash
python demo.py
streamlit run dashboard.py
```

# AI Email Triage Bot

Automatically classifies emails by urgency and drafts replies using AI.

## What it does
- Classifies emails: urgent / follow_up / info / spam
- Drafts a professional 2-sentence reply for each
- Logs all results to CSV
- Shows live metrics in a Streamlit dashboard

## Demo
[Watch 2-minute demo on Loom](YOUR_LOOM_LINK_HERE)

## ROI
- Build time: ~3 hours
- Saves: ~10 hrs/month of manual triage
- Cost: Free (uses Groq API free tier)

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
# Load sample data
python demo.py

# Launch dashboard
streamlit run dashboard.py
```

## Tech stack
- Python, Streamlit, Groq API (llama-3.1-8b-instant)
- CSV logging, real-time dashboard

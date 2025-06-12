# AI Email Triage Bot

Automatically classifies emails by urgency and drafts replies using Claude AI.

## What it does
- Classifies emails: urgent / follow_up / info / spam
- Drafts a professional 2-sentence reply for each
- Logs all results to CSV
- Shows live metrics in a Streamlit dashboard

## ROI
- Build time: ~3 hours
- Saves: ~10 hrs/month of manual triage
- Cost: ~$0.01 per email in API calls

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install anthropic streamlit pandas python-dotenv
```

Add your Anthropic API key to `.env`:
```
ANTHROPIC_API_KEY=your_key_here
```

## Run
```bash
# Load sample data
python demo.py

# Launch dashboard
streamlit run dashboard.py
```

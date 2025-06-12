import streamlit as st
import pandas as pd
import os
from classifier import classify_and_reply, log_result
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Email Triage AI", page_icon="📧", layout="wide")
st.title("📧 AI Email Triage Dashboard")

col1, col2, col3, col4 = st.columns(4)

try:
    df = pd.read_csv("log.csv")
    col1.metric("Emails Processed", len(df))
    col2.metric("Urgent", len(df[df['category'] == 'urgent']))
    col3.metric("Follow-ups", len(df[df['category'] == 'follow_up']))
    col4.metric("Hours Saved Est.", f"{len(df) * 3 / 60:.1f} hrs")

    st.subheader("Category Breakdown")
    st.bar_chart(df['category'].value_counts())

    st.subheader("All Triaged Emails")
    st.dataframe(
        df[['timestamp', 'sender', 'subject', 'category', 'priority', 'draft_reply']],
        use_container_width=True
    )
except FileNotFoundError:
    st.info("No emails yet. Run demo.py first.")

st.divider()
st.subheader("Try it live")
with st.form("live_form"):
    subject = st.text_input("Email subject")
    sender = st.text_input("Sender email")
    body = st.text_area("Email body")
    submitted = st.form_submit_button("Classify this email")
    if submitted and subject and body:
        with st.spinner("Analyzing..."):
            result = classify_and_reply(subject, body, sender)
            log_result(result)
            st.success(f"Category: **{result['category'].upper()}** | Priority: {result['priority']}/5")
            st.write("**Draft reply:**", result['draft_reply'])
            st.write("**Reason:**", result['reason'])

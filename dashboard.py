import streamlit as st
import pandas as pd
import os
from classifier import classify_and_reply, log_result
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Email Triage System",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global */
    body { font-family: 'Inter', sans-serif; }
    .block-container { padding: 2rem 3rem; }

    /* Hide streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Top header bar */
    .header-bar {
        background-color: #0f172a;
        padding: 1.2rem 2rem;
        margin: -2rem -3rem 2rem -3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-title {
        color: #f8fafc;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .header-sub {
        color: #94a3b8;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Metric cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 3px solid #0f172a;
        padding: 1.2rem 1.5rem;
        border-radius: 4px;
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748b;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
    }
    .metric-value.urgent { color: #dc2626; }
    .metric-value.follow { color: #d97706; }
    .metric-value.saved { color: #16a34a; }

    /* Section titles */
    .section-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748b;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Priority badges */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 2px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .badge-urgent { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
    .badge-follow_up { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
    .badge-info { background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }
    .badge-spam { background: #f8fafc; color: #475569; border: 1px solid #cbd5e1; }

    /* Form styling */
    .stTextInput input, .stTextArea textarea {
        border: 1px solid #e2e8f0;
        border-radius: 3px;
        font-size: 0.9rem;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #0f172a;
        box-shadow: none;
    }

    /* Submit button */
    .stButton button {
        background-color: #0f172a;
        color: white;
        border: none;
        border-radius: 3px;
        padding: 0.5rem 1.5rem;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #1e293b;
    }

    /* Result box */
    .result-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0f172a;
        padding: 1.2rem 1.5rem;
        border-radius: 0 4px 4px 0;
        margin-top: 1rem;
    }
    .result-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #94a3b8;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 3px;
    }
    .result-value {
        font-size: 0.95rem;
        color: #0f172a;
        margin-bottom: 0.8rem;
    }

    /* Dataframe */
    .dataframe { font-size: 0.85rem; }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header bar
st.markdown("""
<div class="header-bar">
    <div>
        <div class="header-title">Email Triage System</div>
        <div class="header-sub">Automated Classification and Response Pipeline</div>
    </div>
    <div class="header-sub">Powered by Groq — llama-3.1</div>
</div>
""", unsafe_allow_html=True)

# Load data
try:
    df = pd.read_csv("log.csv")
    has_data = True
except FileNotFoundError:
    has_data = False
    df = pd.DataFrame()

# Metrics row
st.markdown('<div class="section-title">Pipeline Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    count = len(df) if has_data else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Emails Processed</div>
        <div class="metric-value">{count}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    urgent = len(df[df['category'] == 'urgent']) if has_data else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Urgent</div>
        <div class="metric-value urgent">{urgent}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    followup = len(df[df['category'] == 'follow_up']) if has_data else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Follow-ups</div>
        <div class="metric-value follow">{followup}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    spam = len(df[df['category'] == 'spam']) if has_data else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Spam Filtered</div>
        <div class="metric-value">{spam}</div>
    </div>""", unsafe_allow_html=True)

with col5:
    hours = round(count * 3 / 60, 1) if has_data else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Hours Saved</div>
        <div class="metric-value saved">{hours}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 2rem'></div>", unsafe_allow_html=True)

# Two column layout — chart left, table right
if has_data:
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown('<div class="section-title">Category Distribution</div>', unsafe_allow_html=True)
        chart_data = df['category'].value_counts().reset_index()
        chart_data.columns = ['Category', 'Count']
        st.bar_chart(
            chart_data.set_index('Category'),
            color="#0f172a",
            height=260
        )

        st.markdown("<div style='margin-top: 1.5rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Priority Breakdown</div>', unsafe_allow_html=True)
        priority_data = df['priority'].value_counts().sort_index().reset_index()
        priority_data.columns = ['Priority', 'Count']
        st.bar_chart(
            priority_data.set_index('Priority'),
            color="#334155",
            height=200
        )

    with col_right:
        st.markdown('<div class="section-title">Triage Log</div>', unsafe_allow_html=True)
        display_df = df[['timestamp', 'sender', 'subject', 'category', 'priority', 'draft_reply']].copy()
        display_df.columns = ['Timestamp', 'Sender', 'Subject', 'Category', 'Priority', 'Draft Reply']
        display_df = display_df.sort_values('Timestamp', ascending=False)
        st.dataframe(
            display_df,
            use_container_width=True,
            height=520,
            hide_index=True
        )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Live classification
st.markdown('<div class="section-title">Live Classification</div>', unsafe_allow_html=True)

col_form, col_result = st.columns([1, 1])

with col_form:
    subject = st.text_input("Subject", placeholder="Enter email subject")
    sender = st.text_input("Sender", placeholder="sender@company.com")
    body = st.text_area("Body", placeholder="Enter email body", height=140)
    submit = st.button("Run Classification")

with col_result:
    if submit and subject and body:
        with st.spinner("Classifying..."):
            result = classify_and_reply(subject, body, sender)
            log_result(result)

        badge_class = f"badge-{result['category']}"
        category_display = result['category'].replace('_', ' ').title()

        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Classification</div>
            <div class="result-value">
                <span class="badge {badge_class}">{category_display}</span>
                &nbsp;&nbsp;Priority {result['priority']} / 5
            </div>
            <div class="result-label">Reason</div>
            <div class="result-value">{result['reason']}</div>
            <div class="result-label">Draft Reply</div>
            <div class="result-value">{result['draft_reply']}</div>
        </div>
        """, unsafe_allow_html=True)
    elif submit:
        st.warning("Please enter a subject and body to classify.")
    else:
        st.markdown("""
        <div class="result-box" style="border-left-color: #e2e8f0;">
            <div class="result-label">Awaiting Input</div>
            <div class="result-value" style="color: #94a3b8;">
                Fill in the form and click Run Classification to see results here.
            </div>
        </div>
        """, unsafe_allow_html=True)
st.markdown("<div style='margin-top: 3rem'></div>", unsafe_allow_html=True)

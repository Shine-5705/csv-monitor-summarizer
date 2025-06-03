import os
import streamlit as st
import pandas as pd
import requests
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

# Load defaults for SMTP server & port only
ENV_SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
ENV_SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
ENV_MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

st.set_page_config(page_title="📊 CSV Summarizer & Emailer", layout="centered")
st.title("📂 CSV Summarizer + Email Sender")

# Required fields - NO fallback to env
st.subheader("📧 Email Settings (Required)")
user_sender = st.text_input("Sender Email", placeholder="your-email@example.com")
user_receiver = st.text_input("Receiver Email", placeholder="receiver@example.com")
user_password = st.text_input("App Password", type="password", placeholder="App password or email password")

st.subheader("🧠 Mistral API Key (optional)")
user_mistral_key = st.text_input("OpenRouter Mistral API Key", help="Leave blank to use the default key from environment")

uploaded_file = st.file_uploader("📤 Upload a CSV file", type=["csv"])

def summarize_with_mistral(prompt_text, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes CSV data."},
            {"role": "user", "content": f"Summarize this CSV content:\n{prompt_text}"}
        ],
        "max_tokens": 300
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] Failed to summarize with Mistral: {e}"

def send_email(subject, body, attachment, sender, receiver, password):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={attachment.name}")
    msg.attach(part)

    try:
        with smtplib.SMTP(ENV_SMTP_SERVER, ENV_SMTP_PORT) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        return True, "✅ Email sent successfully!"
    except Exception as e:
        return False, f"❌ Failed to send email: {e}"

if uploaded_file:
    st.subheader("📄 Preview")
    try:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        summary_text = f"""
CSV File: {uploaded_file.name}
Rows: {df.shape[0]}, Columns: {df.shape[1]}
Columns: {', '.join(df.columns)}
Sample rows:
{df.head(3).to_string(index=False)}
        """

        if st.button("🔍 Generate Summary"):
            with st.spinner("Summarizing..."):
                api_key = user_mistral_key or ENV_MISTRAL_API_KEY
                if not api_key:
                    st.error("Mistral API key is required (either in input or .env)")
                else:
                    ai_summary = summarize_with_mistral(summary_text, api_key)
                    st.text_area("🧠 Mistral Summary", ai_summary, height=200)

        if st.button("📧 Send Email"):
            missing = []
            if not user_sender.strip():
                missing.append("Sender Email")
            if not user_receiver.strip():
                missing.append("Receiver Email")
            if not user_password.strip():
                missing.append("App Password")
            api_key = user_mistral_key or ENV_MISTRAL_API_KEY
            if not api_key:
                missing.append("Mistral API Key")

            if missing:
                st.error("Missing required fields: " + ", ".join(missing))
            else:
                with st.spinner("Generating summary and sending email..."):
                    ai_summary = summarize_with_mistral(summary_text, api_key)
                    success, message = send_email(
                        subject=f"CSV Summary: {uploaded_file.name}",
                        body=ai_summary,
                        attachment=uploaded_file,
                        sender=user_sender,
                        receiver=user_receiver,
                        password=user_password
                    )
                    st.success(message) if success else st.error(message)

    except Exception as e:
        st.error(f"❌ Failed to read CSV: {e}")

import os
import streamlit as st
import pandas as pd
import requests
import tempfile
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.message import EmailMessage
from dotenv import load_dotenv
from ydata_profiling import ProfileReport

# Load environment variables
load_dotenv()
DEFAULT_MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def summarize_with_mistral(df, mistral_key):
    prompt = f"Summarize the following dataset:\n{df.head(10).to_csv(index=False)}"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {mistral_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"❌ Mistral summarization failed: {e}")
        return "Summary generation failed."


def generate_detailed_text_report(df):
    profile = ProfileReport(df, title="Detailed CSV Analysis", explorative=True)
    
    # Save HTML for UI preview
    html_path = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
    profile.to_file(html_path)

    # Build text summary
    report_text = []
    report_text.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}\n")
    report_text.append("Column Types:\n")
    for col in df.columns:
        report_text.append(f" - {col}: {df[col].dtype}\n")
    report_text.append("\nMissing Values:\n")
    report_text.append(str(df.isnull().sum()))
    report_text.append("\n\nSummary Statistics:\n")
    report_text.append(str(df.describe(include='all')))

    txt_path = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_text))

    return html_path, txt_path


def send_email(sender, receiver, password, subject, body, attachments):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.attach(MIMEText(body, "plain"))

        for filename, filedata in attachments:
            msg.add_attachment(filedata,
                               maintype="application",
                               subtype="octet-stream",
                               filename=filename)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        st.success("✅ Email sent successfully!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")


# Streamlit UI
st.set_page_config(page_title="CSV Summarizer and Emailer")
st.title("📊 CSV Summarizer & Emailer")

# Inputs
sender_email = st.text_input("Sender Email", help="Your Gmail address")
receiver_email = st.text_input("Receiver Email", help="Recipient email address")
app_password = st.text_input("App Password", type="password", help="Generated App Password from Google")
user_mistral_key = st.text_input("Mistral API Key (optional)", help="Use your OpenRouter API key (optional)")

uploaded_file = st.file_uploader("Upload CSV File", type="csv")
detailed_analysis = st.checkbox("Generate Detailed Analysis Report (text + HTML preview)")

with st.expander("🔐 How to get Gmail App Password"):
    st.markdown("""
    1. Go to [Google Account Security](https://myaccount.google.com/security)
    2. Enable **2-Step Verification**
    3. Visit **App Passwords**
    4. Choose **Mail > Windows Computer** or custom name
    5. Copy and paste the 16-character password above
    """)

summary = ""
html_report_path = None
txt_report_path = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 📂 CSV Preview")
    st.dataframe(df)

    if st.button("🧠 Generate Summary"):
        key_to_use = user_mistral_key or DEFAULT_MISTRAL_KEY
        if not key_to_use:
            st.error("Please enter a Mistral API key.")
        else:
            summary = summarize_with_mistral(df, key_to_use)
            st.write("### 📌 Mistral Summary")
            st.write(summary)

    if detailed_analysis:
        st.write("### 🔍 Detailed Analysis Report")
        html_report_path, txt_report_path = generate_detailed_text_report(df)
        with open(html_report_path, "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=500, scrolling=True)

    if st.button("✉️ Send Email"):
        if not (sender_email and receiver_email and app_password):
            st.error("Sender Email, Receiver Email, and App Password are required!")
        else:
            attachments = [(uploaded_file.name, uploaded_file.getvalue())]
            if txt_report_path:
                with open(txt_report_path, "rb") as f:
                    attachments.append(("detailed_report.txt", f.read()))

            body = "📌 Mistral Summary:\n\n" + (summary or "Summary not available.")
            send_email(sender_email, receiver_email, app_password, "📄 CSV Summary & Report", body, attachments)

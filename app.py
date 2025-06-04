import os
import streamlit as st
import pandas as pd
import requests
import tempfile
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from ydata_profiling import ProfileReport
import pdfkit

# Load environment variables
load_dotenv()
DEFAULT_MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
DEFAULT_SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
DEFAULT_SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


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
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Summarization failed: {e}")
        return "Summary generation failed."


def generate_detailed_pdf(df):
    profile = ProfileReport(df, title="Detailed CSV Analysis", explorative=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as html_file:
        profile.to_file(html_file.name)
        pdf_path = html_file.name.replace(".html", ".pdf")
        # Path to wkhtmltopdf executable - adjust if needed
        #path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        #config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        # On Linux (Render), wkhtmltopdf should be installed and in PATH
        config = pdfkit.configuration()  # no path specified


        pdfkit.from_file(html_file.name, pdf_path, configuration=config)
        return pdf_path


def send_email(sender, receiver, password, subject, body, attachments, smtp_server, smtp_port):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content(body)

        for filename, filedata in attachments:
            msg.add_attachment(filedata,
                               maintype="application",
                               subtype="octet-stream",
                               filename=filename)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")


st.title("📊 CSV Summarizer & Emailer")

# Input fields
sender_email = st.text_input("Sender Email", help="Enter your Gmail address")
receiver_email = st.text_input("Receiver Email", help="Enter recipient email address")
app_password = st.text_input("App Password", type="password", help="Gmail App Password (see below)")
user_mistral_key = st.text_input("Mistral API Key (optional)", help="Use your own Mistral API key (optional)")

uploaded_file = st.file_uploader("Upload CSV File", type="csv")
detailed_analysis = st.checkbox("Generate Detailed Analysis Report (as PDF)")

# How to get app password
with st.expander("🔐 How to get Gmail App Password"):
    st.markdown("""
    1. Go to [Google Account Security](https://myaccount.google.com/security)
    2. Enable **2-Step Verification**
    3. Go to **App Passwords**
    4. Choose **Mail** and generate a 16-character password
    5. Use it as the App Password above
    """)

summary = ""
pdf_path = None
df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 🧾 CSV Preview")
    st.dataframe(df)

    if st.button("🧠 Generate Summary"):
        key_to_use = user_mistral_key or DEFAULT_MISTRAL_KEY
        if not key_to_use:
            st.error("No Mistral API key provided. Please enter one.")
        else:
            summary = summarize_with_mistral(df, key_to_use)
            st.write("### 📌 Summary")
            st.write(summary)

    if detailed_analysis:
        st.write("### 📈 Generating Detailed Analysis PDF...")
        try:
            pdf_path = generate_detailed_pdf(df)
            st.success("Detailed analysis report generated as PDF.")
        except Exception as e:
            st.error(f"Failed to generate PDF: {e}")

    if st.button("✉️ Send Email"):
        if not (sender_email and receiver_email and app_password):
            st.error("Sender, Receiver, and App Password are required!")
        else:
            key_to_use = user_mistral_key or DEFAULT_MISTRAL_KEY
            if not key_to_use:
                st.error("No Mistral API key provided. Please enter one.")
            else:
                # Generate summary if empty before sending email
                if not summary:
                    with st.spinner("Generating summary..."):
                        summary = summarize_with_mistral(df, key_to_use)
                        st.write("### 📌 Summary")
                        st.write(summary)

                attachments = [(uploaded_file.name, uploaded_file.getvalue())]
                if pdf_path:
                    with open(pdf_path, "rb") as f:
                        attachments.append(("detailed_report.pdf", f.read()))

                send_email(
                    sender=sender_email,
                    receiver=receiver_email,
                    password=app_password,
                    subject="CSV Summary & Analysis",
                    body=summary or "See attached analysis.",
                    attachments=attachments,
                    smtp_server=DEFAULT_SMTP_SERVER,
                    smtp_port=DEFAULT_SMTP_PORT
                )

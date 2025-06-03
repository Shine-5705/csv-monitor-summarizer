import os
import time
import smtplib
import pandas as pd
import requests
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ENV
FOLDER_PATH = "csv_folder"
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
USE_MISTRAL = os.getenv("USE_MISTRAL", "False") == "True"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# --- OpenRouter Mistral Summarization ---
def summarize_with_mistral(summary_text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes CSV data."},
            {"role": "user", "content": f"Summarize this CSV content:\n{summary_text}"}
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"OpenRouter summarization failed: {e}")
        return summary_text

# --- Email ---
def send_email(subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach file if provided
    if attachment_path:
        try:
            with open(attachment_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(part)
            logging.info(f"Attached file: {attachment_path}")
        except Exception as e:
            logging.warning(f"Failed to attach file: {e}")

    # Retry logic
    for attempt in range(3):
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            logging.info("Email sent successfully.")
            return
        except Exception as e:
            logging.error(f"Failed to send email (Attempt {attempt + 1}/3): {e}")
            time.sleep(2)
    logging.critical("All email attempts failed.")

# --- CSV Summary ---
def summarize_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        num_rows, num_cols = df.shape
        column_names = df.columns.tolist()
        preview = df.head(3).to_string(index=False)

        summary = f"""CSV File Summary:
- File: {os.path.basename(file_path)}
- Rows: {num_rows}
- Columns: {num_cols}
- Column Names: {', '.join(column_names)}

Sample Rows:
{preview}
"""

        if USE_MISTRAL:
            summary = summarize_with_mistral(summary)

        return summary
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        return "[ERROR] Failed to read CSV."

# --- File Watcher ---
class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            logging.info(f"New CSV detected: {event.src_path}")
            summary = summarize_csv(event.src_path)
            send_email(
                subject="New CSV Summary",
                body=summary,
                attachment_path=event.src_path
            )

# --- Monitor Start ---
def start_monitoring():
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_PATH, recursive=False)
    observer.start()
    logging.info(f"Monitoring started on folder: {FOLDER_PATH}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()

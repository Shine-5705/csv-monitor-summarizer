import os
import time
import smtplib
import pandas as pd
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

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
        print(f"[ERROR] OpenRouter summarization failed: {e}")
        return summary_text

# --- Email ---
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("[INFO] Email sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

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
        return f"[ERROR] Failed to read CSV: {e}"

# --- File Watcher ---
class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            print(f"[INFO] New CSV detected: {event.src_path}")
            summary = summarize_csv(event.src_path)
            send_email(subject="New CSV Summary", body=summary)

def start_monitoring():
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_PATH, recursive=False)
    observer.start()
    print(f"[INFO] Monitoring started on folder: {FOLDER_PATH}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()

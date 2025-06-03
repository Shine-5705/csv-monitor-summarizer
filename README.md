# CSV Summarizer & Emailer

A simple Streamlit application that allows you to upload CSV files, automatically generate a summary of their content using the [Mistral](https://mistral.ai/) language model via OpenRouter API, and send the summary along with the CSV file as an email attachment.

---

## Application Preview

![Streamlit CSV Summarizer UI Screenshot](assets\ui.png)

<details>
<summary>Demo Video</summary>

<!-- Replace the URL below with your actual demo video link -->

[![CSV Summarizer Demo Video](https://img.youtube.com/vi/your-video-id/0.jpg)](https://www.youtube.com/watch?v=your-video-id)

</details>

---

## Features

- Upload CSV files and preview content.
- Automatically summarize CSV data with Mistral AI.
- Send email with summary and CSV file attached.
- Supports custom sender & receiver emails with app password.
- Optional Mistral API key input (falls back to `.env`).

---

## Getting Started

### Prerequisites

- Python 3.7+
- Streamlit (`pip install streamlit`)
- Requests library (`pip install requests`)
- Python dotenv (`pip install python-dotenv`)
- Pandas (`pip install pandas`)

### Setup

1. Create a `.env` file in the project root with the following variables:

    ```env
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    MISTRAL_API_KEY=your_default_mistral_api_key_here
    ```

2. Run the Streamlit app:

    ```bash
    streamlit run csv_summarizer_app.py
    ```

---

## Usage

1. Open the Streamlit web interface.
2. Fill in the **Sender Email**, **Receiver Email**, and **App Password** fields (required).
3. Optionally enter your Mistral API key or leave it blank to use the one from `.env`.
4. Upload a CSV file.
5. Click **Generate Summary** to see the AI-generated summary.
6. Click **Send Email** to send the summary and the CSV file to the receiver.

---

## How to Get an App Password (for Gmail)

To send emails securely, use an **App Password** instead of your main Gmail password. Here are the steps:

1. Go to your [Google Account Security Settings](https://myaccount.google.com/security).
2. Ensure **2-Step Verification** is **enabled**. If not, enable it first.
3. Under **"Signing in to Google"**, click **App passwords**.
4. Select **Mail** as the app and your device (e.g., Windows Computer), then click **Generate**.
5. Copy the 16-character app password displayed and use it in the app’s **App Password** field.
6. Keep this password safe; it can only be viewed once.

> **Note:** Using app passwords helps keep your account secure by not sharing your main password with third-party apps.

---

## Security Notes

Your email credentials are used only in-memory to send the email via SMTP. Do not share your app password with others. Always use app-specific passwords instead of your main email password.

---

## Troubleshooting

- Make sure your email account allows SMTP access and app passwords are enabled.
- If summary generation fails, verify your Mistral API key and internet connectivity.
- Check terminal logs for error messages.

---

## License

MIT License © 2025 Shine gupta
---

*Created with ❤️ using Python, Streamlit, and Mistral AI*

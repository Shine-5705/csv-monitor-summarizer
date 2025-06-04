# CSV Summarizer & Emailer

A simple **Streamlit application** that empowers you to **quickly analyze and share insights** from your CSV data using advanced AI summarization via the [Mistral](https://mistral.ai/) language model. Upload your CSV files, get concise summaries instantly, and send those insights directly via email — all from a clean and intuitive web interface.

---

## Why Use This App?

- **Save Time:** Instantly get summaries of large CSV datasets without manually reading rows and columns.
- **Better Communication:** Share key insights with colleagues or stakeholders via email, including the original CSV for reference.
- **Customizable & Secure:** Input your own sender, receiver, and secure app password. Mistral API key is optional — use the default or your own.
- **User-Friendly:** No coding required! Everything works from a web UI built with Streamlit.
- **Flexible:** Supports any CSV file with tabular data, making it useful across domains — business reports, data audits, research, finance, and more.

---

## Application Preview

![Streamlit CSV Summarizer UI Screenshot](https://github.com/Shine-5705/csv-monitor-summarizer/blob/main/assets/ui.png)

<details>
<summary>Demo Video</summary>

[![CSV Summarizer Demo Video](https://img.youtube.com/vi/your-video-id/0.jpg)](https://www.youtube.com/watch?v=your-video-id)

</details>

---

## Features

- Upload and preview CSV files easily.
- Generate AI-powered summaries to grasp data highlights quickly.
- Email summaries with the original CSV attached.
- Support for custom email credentials for secure SMTP sending.
- Optionally use your own Mistral API key or default from environment variables.

---

## Getting Started

### Prerequisites

- Python 3.7+
- Streamlit (`pip install streamlit`)
- Requests (`pip install requests`)
- Python dotenv (`pip install python-dotenv`)
- Pandas (`pip install pandas`)

### Setup

1. Create a `.env` file in the project root with:

    ```env
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    MISTRAL_API_KEY=your_default_mistral_api_key_here
    ```

2. Run the app with:

    ```bash
    streamlit run csv_summarizer_app.py
    ```

---

## How to Use

1. Open the app in your browser.
2. Enter **Sender Email**, **Receiver Email**, and **App Password** (required for sending emails).
3. Optionally enter your **Mistral API key** or leave blank to use the default key.
4. Upload a CSV file to analyze.
5. Click **Generate Summary** to see AI insights.
6. Click **Send Email** to share the summary and CSV.

---

## How to Get an App Password (Gmail)

1. Go to your [Google Account Security](https://myaccount.google.com/security).
2. Enable **2-Step Verification** if not already done.
3. Click **App Passwords** under "Signing in to Google".
4. Choose **Mail** and your device, then click **Generate**.
5. Copy the generated 16-character password into the app's **App Password** field.

> **Tip:** Use app passwords instead of your main password for better security.

---

## Benefits Summary

- **For Data Analysts & Managers:** Quickly summarize datasets and email insights to your team.
- **For Researchers:** Share clean summaries and raw data in one step.
- **For Businesses:** Speed up report sharing with minimal effort.
- **For Everyone:** No need to write code or deal with complex email setups.

---

## Troubleshooting

- Check SMTP and email credentials.
- Verify Mistral API key validity.
- Monitor terminal logs for detailed errors.

---

## License

MIT License © 2025 Shine Gupta

---

*Built with ❤️ using Python, Streamlit, and Mistral AI*


# CSV Summarizer & Emailer

A simple **Streamlit application** that empowers you to **quickly analyze and share insights** from your CSV data using advanced AI summarization via the [Mistral](https://mistral.ai/) language model. Upload your CSV files, get concise summaries instantly, and send those insights directly via email — all from a clean and intuitive web interface.

---

## 🚀 What's New

✅ **Mistral Summary in Email Body**  
✅ **PDF Report Generation**  
✅ **CSV File Sent as Email Attachment**  
✅ **Fully Editable Sender/Receiver Fields**  
✅ **.env Support for Secret Management**  
✅ **One-Click Email Sending with Insights + Attachments**  

---

## 💡 Why Use This App?

- **Save Time:** Instantly get summaries of large CSV datasets without manually reading rows and columns.
- **Better Communication:** Share key insights with colleagues or stakeholders via email, including the original CSV for reference.
- **Customizable & Secure:** Input your own sender, receiver, and secure app password. Mistral API key is optional — use the default or your own.
- **User-Friendly:** No coding required! Everything works from a web UI built with Streamlit.
- **Flexible:** Supports any CSV file with tabular data, making it useful across domains — business reports, data audits, research, finance, and more.

---

## 📸 Application Preview

![Streamlit CSV Summarizer UI Screenshot](https://github.com/Shine-5705/csv-monitor-summarizer/blob/main/assets/image.png)

<details>
<summary>🎥 Demo Video</summary>

[![CSV Summarizer Demo Video](https://img.youtube.com/vi/your-video-id/0.jpg)](https://www.youtube.com/watch?v=your-video-id)

</details>

---

## ✨ Features

- 📤 Upload and preview CSV files.
- 🤖 Generate Mistral AI summaries to grasp insights instantly.
- 📧 Send emails with:
  - 📝 AI-generated summary in the **email body**
  - 📎 Attached CSV and **PDF report** of the summary
- 🔐 Secure email using Gmail SMTP and App Passwords.
- 🔄 Supports `.env` secrets or manual entry.
- 💻 Clean, responsive UI built using Streamlit.

---

## ⚙️ Getting Started

### ✅ Prerequisites

- Python 3.7+
- Install dependencies:

```bash
pip install streamlit pandas requests ydata-profiling pdfkit python-dotenv
```
or 
```bash
pip install -r requirements.txt
```

- Install `wkhtmltopdf` for PDF export:  
  👉 [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)

> Ensure it's installed to:
> `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe` (or adjust path in code)

---

### 📁 .env Setup

Create a `.env` file in your project root:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
MISTRAL_API_KEY=your_default_mistral_api_key
```

---

### ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧠 How to Use

1. Open the app in your browser.
2. Enter:
   - **Sender Email**
   - **Receiver Email**
   - **App Password**
3. (Optional) Enter your own **Mistral API Key**
4. Upload a `.csv` file
5. Click **Generate Summary** to preview insights.
6. Click **Send Email** to deliver:
   - ✉️ Email with summary in body
   - 📎 CSV + PDF summary as attachments

---

## 🔐 How to Get a Gmail App Password

1. Visit [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**
3. Under "Signing in to Google", click **App Passwords**
4. Select **Mail > Your Device**
5. Copy the 16-character password into the app

> 🛡️ Use App Passwords — never your main Gmail password.

---

## 💼 Use Cases

- **Data Analysts**: Quickly summarize and share insights.
- **Managers**: Automate email reports.
- **Researchers**: Collaborate with clean, AI-powered summaries.
- **Startups**: Improve communication with auto-generated insights.
- **Educators & Students**: Share datasets and summaries in one go.

---

## 🐛 Troubleshooting

- Check `SMTP_SERVER`, port, and credentials.
- Ensure `wkhtmltopdf` is installed correctly.
- Confirm Mistral API Key is valid.
- Monitor Streamlit logs in terminal for errors.

---

## 🧪 Developer Notes

To deploy on [Streamlit Cloud](https://share.streamlit.io):

- Push `app.py`, `requirements.txt`, `.env.example` to GitHub
- Add secrets in Streamlit Cloud:
  ```env
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  MISTRAL_API_KEY=your_key
  ```

> **Optional:** Bundle the app with `pyinstaller` for an executable.

---

## 📝 License

MIT License © 2025 Shine Gupta

---

**Built with ❤️ using Python, Streamlit, and Mistral AI**

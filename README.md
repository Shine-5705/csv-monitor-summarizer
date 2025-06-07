# CSV Summarizer & Emailer

A simple **Streamlit application** that empowers you to **quickly analyze and share insights** from your CSV data using advanced AI summarization via the [Mistral](https://mistral.ai/) language model. Upload your CSV files, get concise summaries instantly, and send those insights directly via email — including a **PDF report and the original CSV**.

🟢 **Live On:** [https://csv-summarizer-emailer.onrender.com](https://csv-summarizer-emailer.onrender.com)

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

- **Save Time:** Instantly get summaries of large CSV datasets.
- **Better Communication:** Share insights + PDF + CSV in one email.
- **Customizable & Secure:** Your own sender, receiver, and secure keys.
- **User-Friendly:** No coding required! Clean UI built with Streamlit.
- **Flexible:** Useful across business, research, education, and more.

---

## 📸 Application Preview

![Streamlit CSV Summarizer UI Screenshot](https://github.com/Shine-5705/csv-monitor-summarizer/blob/main/assets/image.png)

<details>
<summary>🎥 Demo Video</summary>

[![CSV Summarizer Demo Video🎥](https://youtu.be/-lqke84Vpug)](https://youtu.be/-lqke84Vpug)

</details>

---

## ✨ Features

- 📤 Upload and preview CSV files
- 🤖 Generate AI summary using Mistral
- 📧 Send emails with:
  - ✅ Summary in email **body**
  - 📎 Attached CSV file
  - 📄 **PDF summary report**
- 🔐 Secure Gmail SMTP using App Passwords
- 🛠️ Supports `.env` secrets or manual entry
- 💻 Streamlit-based, responsive UI

---

## ⚙️ Getting Started Locally

### ✅ Prerequisites

- Python 3.7+
- Install dependencies:

```bash
pip install -r requirements.txt
```

Install wkhtmltopdf (used to export PDF):

👉 https://wkhtmltopdf.org/downloads.html

Example path: `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`
(Update this in app.py if needed.)

### 📁 .env Setup
Create a `.env` file in the project root:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
MISTRAL_API_KEY=your_default_mistral_api_key
```

### ▶️ Run the App Locally
```bash
streamlit run app.py
```

---

## 🐳 Docker Deployment (Recommended for Production)

This app is ready for containerized deployment using Docker.

### 📦 Build and Run Locally
```bash
docker build -t csv-summarizer .
docker run -p 8501:8501 --env-file .env csv-summarizer
```
Visit: http://localhost:8501

### 🚀 Deploy to Render (Docker Setup)

1. Push code to GitHub
2. Go to Render
3. Create a new Web Service
4. Use:
   - Environment: Docker
   - Build Command: Leave blank
   - Start Command: auto-detected from Dockerfile
5. Add environment variables from your `.env`

✅ **Done!** Your app will be live at:
https://csv-summarizer-emailer.onrender.com

---

## 🧠 How to Use

1. Open the app in your browser
2. Fill in:
   - 📤 Sender Email
   - 📥 Receiver Email
   - 🔑 Gmail App Password
   - (Optional) 🧠 Mistral API Key
3. Upload a `.csv` file
4. Click **Generate Summary**
5. Click **Send Email** to deliver:
   - 📄 Summary in email body
   - 📎 CSV + PDF report as attachments

---

## 🔐 How to Get a Gmail App Password

1. Visit Google Account Security
2. Enable 2-Step Verification
3. Click **App Passwords**
4. Select **Mail > Custom Device**
5. Copy the generated 16-character password

⚠️ **Use App Passwords** — not your main Gmail password.

---

## 💼 Use Cases

- 📊 **Data Analysts:** Share summaries with teams
- 🧑‍💼 **Managers:** Auto-email CSV reports
- 🧪 **Researchers:** Summarize and email experiments
- 🚀 **Startups:** Communicate insights effortlessly
- 🎓 **Students & Educators:** Auto-document data analysis

---

## 🐛 Troubleshooting

- Check Gmail SMTP, App Password, and email permissions
- Ensure wkhtmltopdf is installed and path is correct
- Watch terminal logs for Streamlit + SMTP errors

---

## 📝 License

MIT License © 2025 Shine Gupta

Built with ❤️ using Python, Streamlit, Mistral, and Gmail SMTP
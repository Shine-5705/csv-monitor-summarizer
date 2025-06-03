<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>CSV Summarizer & Emailer - README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: auto;
            padding: 2rem;
            line-height: 1.6;
            background: #f9f9f9;
            color: #333;
        }
        h1, h2 {
            color: #2c3e50;
        }
        code {
            background: #eee;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: Consolas, monospace;
        }
        pre {
            background: #eee;
            padding: 1rem;
            border-radius: 5px;
            overflow-x: auto;
        }
        a {
            color: #2980b9;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .note {
            background: #eaf4ff;
            border-left: 5px solid #2980b9;
            padding: 0.8em 1em;
            margin: 1em 0;
            color: #555;
        }
        img {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 0 6px rgba(0,0,0,0.15);
            margin-bottom: 1rem;
        }
        .video-container {
            position: relative;
            padding-bottom: 56.25%;
            padding-top: 30px;
            height: 0;
            overflow: hidden;
            margin-bottom: 2rem;
        }
        .video-container iframe, 
        .video-container object, 
        .video-container embed {
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
        }
    </style>
</head>
<body>
    <h1>CSV Summarizer & Emailer</h1>
    <p>
        A simple Streamlit application that allows you to upload CSV files, automatically generate a summary of their content using
        the <a href="https://mistral.ai/" target="_blank" rel="noopener">Mistral</a> language model via OpenRouter API,
        and send the summary along with the CSV file as an email attachment.
    </p>

    <h2>Application Preview</h2>
    <img src="ui_screenshot.png" alt="Streamlit CSV Summarizer UI Screenshot" />
    <div class="video-container">
        <!-- Replace the src URL below with your actual demo video link -->
        <iframe src="https://www.youtube.com/embed/your-video-id" frameborder="0" allowfullscreen title="CSV Summarizer Demo"></iframe>
    </div>

    <h2>Features</h2>
    <ul>
        <li>Upload CSV files and preview content.</li>
        <li>Automatically summarize CSV data with Mistral AI.</li>
        <li>Send email with summary and CSV file attached.</li>
        <li>Supports custom sender & receiver emails with app password.</li>
        <li>Optional Mistral API key input (falls back to <code>.env</code>).</li>
    </ul>

    <h2>Getting Started</h2>
    <h3>Prerequisites</h3>
    <ul>
        <li>Python 3.7+</li>
        <li>Streamlit (<code>pip install streamlit</code>)</li>
        <li>Requests library (<code>pip install requests</code>)</li>
        <li>Python dotenv (<code>pip install python-dotenv</code>)</li>
        <li>Pandas (<code>pip install pandas</code>)</li>
    </ul>

    <h3>Setup</h3>
    <ol>
        <li>Create a <code>.env</code> file in the project root with the following variables:
            <pre>
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
MISTRAL_API_KEY=your_default_mistral_api_key_here
            </pre>
        </li>
        <li>Run the Streamlit app:
            <pre>streamlit run csv_summarizer_app.py</pre>
        </li>
    </ol>

    <h2>Usage</h2>
    <ol>
        <li>Open the Streamlit web interface.</li>
        <li>Fill in the <strong>Sender Email</strong>, <strong>Receiver Email</strong>, and <strong>App Password</strong> fields (required).</li>
        <li>Optionally enter your Mistral API key or leave it blank to use the one from <code>.env</code>.</li>
        <li>Upload a CSV file.</li>
        <li>Click <strong>Generate Summary</strong> to see the AI-generated summary.</li>
        <li>Click <strong>Send Email</strong> to send the summary and the CSV file to the receiver.</li>
    </ol>

    <h2>How to Get an App Password (for Gmail)</h2>
    <p>To send emails securely, use an <strong>App Password</strong> instead of your main Gmail password. Here are the steps:</p>
    <ol>
        <li>Go to your <a href="https://myaccount.google.com/security" target="_blank" rel="noopener">Google Account Security Settings</a>.</li>
        <li>Ensure <strong>2-Step Verification</strong> is <em>enabled</em>. If not, enable it first.</li>
        <li>Under <strong>"Signing in to Google"</strong>, click <strong>App passwords</strong>.</li>
        <li>Select <em>Mail</em> as the app and your device (e.g., Windows Computer), then click <strong>Generate</strong>.</li>
        <li>Copy the 16-character app password displayed and use it in the app’s <strong>App Password</strong> field.</li>
        <li>Keep this password safe; it can only be viewed once.</li>
    </ol>
    <p class="note">
        Using app passwords helps keep your account secure by not sharing your main password with third-party apps.
    </p>

    <h2>Security Notes</h2>
    <p class="note">
        Your email credentials are used only in-memory to send the email via SMTP. Do not share your app password with others.
        Always use app-specific passwords instead of your main email password.
    </p>

    <h2>Troubleshooting</h2>
    <ul>
        <li>Make sure your email account allows SMTP access and app passwords are enabled.</li>
        <li>If summary generation fails, verify your Mistral API key and internet connectivity.</li>
        <li>Check terminal logs for error messages.</li>
    </ul>

    <h2>License</h2>
    <p>MIT License &copy; 2025 Shine Gupta</p>

    <footer>
        <p>Created with ❤️ using Python, Streamlit, and Mistral AI</p>
    </footer>
</body>
</html>

# 🧠 AI Quiz Generator

An interactive MCQ quiz generator powered by Claude AI (Anthropic). Enter any topic, choose difficulty and number of questions, and get a full quiz instantly.

## 🎥 Demo

> Live app: [your-app-name.streamlit.app](https://your-app-name.streamlit.app) ← update this after deploying

---

## ✨ Features

- Generate MCQs on **any topic** instantly using AI
- Choose **difficulty** (Easy / Medium / Hard)
- Choose **number of questions** (3, 5, 8, or 10)
- Navigate between questions freely before submitting
- Detailed **results page** with score and answer review

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python) |
| AI Model | Claude claude-sonnet-4-20250514 via Anthropic API |
| Language | Python 3.10+ |
| Deployment | Streamlit Cloud |

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/ai-quiz-generator.git
cd ai-quiz-generator
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Create a file at `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

**4. Run the app**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and sign in with GitHub
3. Click **New app** → select this repo → set main file as `app.py`
4. Under **Advanced settings → Secrets**, add:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```
5. Click **Deploy** — your app will be live in under a minute!

---

## 📁 Project Structure

```
ai-quiz-generator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🔑 Getting an API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in
3. Navigate to **API Keys** and create a new key
4. Anthropic gives free credits to new accounts

---

## 👤 Author

Built by [Your Name] as a work sample for an AI internship application.

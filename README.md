# 🧠 Smart AI Tasks API

![Smart AI Tasks Banner](https://github.com/user-attachments/assets/13eb3fbe-ee10-419c-b9f9-234381079c28)

🎥 **Preview:** [Watch Demo Video](https://drive.google.com/file/d/1tzWPgDr1_kMtZitP_WCB9lPA-Hlx3DB1/view?usp=sharing)

A Django-powered backend that transforms messy user-generated inputs (WhatsApp messages, emails, notes) into structured, prioritized tasks using intelligent AI processing. Supports task filtering, import/export, and even ICS calendar generation.

---

## 📍 Live API Documentation

📄 [View Postman API Docs](https://documenter.getpostman.com/view/38405494/2sB34cnhXn)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MadhuSuniL/smart_ai_tasks_api.git
cd smart_ai_tasks_api
````

---

### 2️⃣ Create and Activate Virtual Environment

```bash
# macOS / Linux
python3 -m venv env
source env/bin/activate

# Windows
python -m venv env
env\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

> You can also include optional environment variables for database or external services.

---

### 5️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

### 7️⃣ Run Development Server

```bash
python manage.py runserver
```

🌐 Open in browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## ✅ Features Overview

* ✍️ Context ingestion from WhatsApp, Email, Notes
* 🧠 AI-driven task summarization and priority scoring
* 📊 Filtering by priority, status, and category
* 📎 CSV import/export for task portability
* 📅 ICS calendar file export (for Google Calendar)
* 🔐 Token-based authentication
* 🚀 Ready-to-integrate with React (Next.js) frontend

---

## ⚙️ Core Endpoints

All API routes and schema examples are available in Postman docs:

📑 [API Documentation →](https://documenter.getpostman.com/view/38405494/2sB34cnhXn)

---

## 🤖 Built-in AI Capabilities

The backend leverages AI modules to:

* Summarize long-form user inputs
* Infer sentiment: **Urgent**, **High Stress**, **Casual**
* Classify tasks by category and urgency
* Generate structured task objects from raw text

---

## 👨‍💻 Author

**Madhu Sunil**
🔗 GitHub: [@MadhuSuniL](https://github.com/MadhuSuniL)


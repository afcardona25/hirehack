
# HireHack MVP

This is the MVP of **HireHack**, a tool that rewrites a candidate's CV to match a specific job description using AI and keyword optimization.

## 📁 Project Structure

```
hirehack-mvp/
├── backend/
│   ├── app.py              # Flask backend
│   ├── requirements.txt    # Python dependencies
│   └── .env                # API keys and config (ignored in git)
├── frontend/
│   ├── index.html          # Main interface
│   └── static/
│       ├── style.css       # Styles
│       └── script.js       # JavaScript logic
└── venv/                   # Virtual environment (optional, not committed)
```

---

## 🛠️ Setup Instructions

### 1. Clone / Navigate to the project

```bash
cd path/to/hirehack-mvp
```

### 2. Create and activate virtual environment

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

If `requirements.txt` doesn't exist, you can install manually:

```bash
pip install flask python-dotenv
```

Then optionally save them:

```bash
pip freeze > backend/requirements.txt
```

---

### 4. Environment variables

Create a `.env` file inside `backend/` (if using OpenAI later):

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 5. Run the Flask app

From inside the `backend/` folder:

```bash
cd backend
flask run
```

By default the app will be available at:  
👉 http://127.0.0.1:5000

---

## 🧪 Testing the App

- Make sure your frontend is correctly configured to load static assets using Flask's `url_for`.
- All rewritten content is shown below the form.
- Users can copy or download the result.

---

## ✅ To deactivate virtual environment

```bash
deactivate
```

---

## 📌 Notes

- Do not commit the `venv/` or `.env` files.
- Make sure to always activate the virtual environment before running `flask`.


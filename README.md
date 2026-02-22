# AI Resume Skill Gap & ATS Optimization System

AI-powered full-stack web application that analyzes resumes and checks how well they match a selected job role.

The system extracts skills from a resume (PDF), compares them with role-based requirements, calculates match percentage, identifies missing skills, and generates ATS improvement suggestions.

---

## 🚀 Features

- Resume PDF Upload
- NLP-based Skill Extraction (spaCy)
- Role-Based Skill Comparison
- Match Percentage Calculation
- Skill Gap Detection
- ATS Improvement Suggestions
- Role Recommendation Engine

---

## 🛠 Tech Stack

Frontend:
- React.js
- JavaScript
- CSS

Backend:
- FastAPI
- spaCy (NLP)
- PyMuPDF (PDF parsing)
- Uvicorn

---

## ⚙️ How to Run Locally

### Run Backend

1. Open terminal and go to backend folder:

cd backend

2. Create virtual environment:

python -m venv venv

3. Activate environment (Windows):

venv\Scripts\activate

4. Install dependencies:

pip install -r requirements.txt

5. Start backend server:

uvicorn main:app --reload

Backend runs at:
http://127.0.0.1:8000

---

### Run Frontend

Open a new terminal and run:

cd frontend
npm install
npm start

Frontend runs at:
http://localhost:3000

---

## 👨‍💻 Author

Anshuman Singh  
IBM Internship Project
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import fitz
import spacy

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


@app.get("/")
def home():
    return {"message": "AI Resume Skill Gap & ATS Optimization System Running"}


# ----------------------------
# ROLE SKILL DATASET
# ----------------------------
ROLE_SKILLS = {
    "software_developer": [
        "java", "data structures", "algorithms", "oop",
        "mysql", "git", "github", "html", "css",
        "javascript", "react", "system design", "problem solving"
    ],

    "data_analyst": [
        "python", "sql", "statistics", "machine learning",
        "power bi", "tableau", "data visualization",
        "excel", "communication"
    ],

    "full_stack_developer": [
        "javascript", "react", "node", "express",
        "mongodb", "mysql", "html", "css",
        "rest api", "git", "github"
    ],

    "backend_developer": [
        "java", "spring", "node", "express",
        "database", "mysql", "mongodb",
        "rest api", "system design"
    ],

    "frontend_developer": [
        "html", "css", "javascript", "react",
        "redux", "ui", "responsive design"
    ],

    "machine_learning_engineer": [
        "python", "machine learning", "deep learning",
        "pandas", "numpy", "scikit", "model evaluation"
    ]
}


# ----------------------------
# PDF Text Extraction
# ----------------------------
def extract_text_from_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


# ----------------------------
# NLP Preprocessing
# ----------------------------
def preprocess_text(text):
    doc = nlp(text.lower())
    cleaned_tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(cleaned_tokens)


# ----------------------------
# Skill Gap Analysis
# ----------------------------
def analyze_skill_gap(cleaned_resume_text, role):
    matched_skills = []
    missing_skills = []

    role_skills = ROLE_SKILLS.get(role, [])

    for skill in role_skills:
        skill_doc = nlp(skill.lower())
        skill_lemma = " ".join([token.lemma_ for token in skill_doc])

        if skill_lemma in cleaned_resume_text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(role_skills) > 0:
        match_percentage = round(
            (len(matched_skills) / len(role_skills)) * 100, 2
        )
    else:
        match_percentage = 0

    return match_percentage, matched_skills, missing_skills


# ----------------------------
# Roadmap Generator
# ----------------------------
def generate_roadmap(missing_skills):
    roadmap = []

    for skill in missing_skills:
        roadmap.append({
            "skill": skill,
            "plan": {
                "week_1": f"Study fundamentals of {skill}.",
                "week_2": f"Build a small project using {skill}.",
                "practice": f"Practice interview questions related to {skill}."
            }
        })

    return roadmap


# ----------------------------
# ATS Optimization Suggestions
# ----------------------------
def generate_ats_suggestions(cleaned_resume_text, role):
    suggestions = []

    role_skills = ROLE_SKILLS.get(role, [])

    for skill in role_skills:
        skill_doc = nlp(skill.lower())
        skill_lemma = " ".join([token.lemma_ for token in skill_doc])

        if skill_lemma not in cleaned_resume_text:
            suggestions.append(
                f"Consider adding or strengthening '{skill}' if applicable."
            )

    return suggestions[:5]


# ----------------------------
# Role Recommendation Engine
# ----------------------------
def recommend_roles(cleaned_resume_text):
    role_scores = []

    for role_name, skills in ROLE_SKILLS.items():
        matched = 0

        for skill in skills:
            skill_doc = nlp(skill.lower())
            skill_lemma = " ".join([token.lemma_ for token in skill_doc])

            if skill_lemma in cleaned_resume_text:
                matched += 1

        if len(skills) > 0:
            match_percentage = round((matched / len(skills)) * 100, 2)
        else:
            match_percentage = 0

        role_scores.append({
            "role": role_name,
            "match": match_percentage
        })

    role_scores.sort(key=lambda x: x["match"], reverse=True)

    return role_scores[:3]   # Top 3 roles


# ----------------------------
# MAIN ANALYSIS ENDPOINT
# ----------------------------
@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...),
    role: str = Form(...)
):
    file_bytes = await file.read()

    # Extract & Clean Resume
    raw_resume_text = extract_text_from_pdf(file_bytes)
    cleaned_resume = preprocess_text(raw_resume_text)

    # Skill Gap
    match_percentage, matched_skills, missing_skills = analyze_skill_gap(
        cleaned_resume, role
    )

    # Roadmap
    roadmap = generate_roadmap(missing_skills)

    # ATS Suggestions
    ats_suggestions = generate_ats_suggestions(cleaned_resume, role)

    # Role Recommendation
    recommended_roles = recommend_roles(cleaned_resume)

    return {
        "role_selected": role,
        "skill_match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "learning_roadmap": roadmap,
        "ats_suggestions": ats_suggestions,
        "recommended_roles": recommended_roles
    }

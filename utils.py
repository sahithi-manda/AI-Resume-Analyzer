import PyPDF2
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os

# Ensure spacy model is downloaded
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(reader.pages)):
        page_text = reader.pages[page].extract_text()
        if page_text:
            text += page_text + " "
    return text

def extract_skills(text, skills_csv_path='skills.csv'):
    """Extracts technical and soft skills from text based on a CSV dictionary."""
    try:
        skills_df = pd.read_csv(skills_csv_path)
        skills_list = skills_df['skill'].tolist()
    except Exception as e:
        skills_list = ["Python", "Java", "C++", "React", "Node.js", "SQL", "Machine Learning", "AWS", "Git"] # Fallback
        
    text_lower = text.lower()
    found_skills = []
    
    for skill in skills_list:
        # Use regex for exact word boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
            
    return list(set(found_skills))

def calculate_ats_score(resume_text, jd_text=""):
    """Calculates an ATS score based on JD match or general resume quality."""
    if not jd_text.strip():
        # General resume quality score if no JD is provided
        score = 40
        if len(resume_text.split()) > 200: score += 20
        if len(resume_text.split()) > 400: score += 10
        if re.search(r'\b(experience|work history)\b', resume_text.lower()): score += 10
        if re.search(r'\b(education|academic)\b', resume_text.lower()): score += 10
        if re.search(r'\b(skills|technologies)\b', resume_text.lower()): score += 10
        return min(score, 100)
    
    # Cosine similarity matching if JD is provided
    texts = [resume_text.lower(), jd_text.lower()]
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        score = round(similarity * 100, 2)
        # Boost score slightly as TF-IDF can be harsh
        return min(score + 20, 100) 
    except ValueError:
        return 0

def get_missing_keywords(resume_skills, jd_text, skills_csv_path='skills.csv'):
    """Finds skills present in JD but missing in the resume."""
    if not jd_text.strip():
        return []
    jd_skills = extract_skills(jd_text, skills_csv_path)
    resume_skills_lower = [s.lower() for s in resume_skills]
    
    missing = [skill for skill in jd_skills if skill.lower() not in resume_skills_lower]
    return missing

def predict_category(text):
    """Predicts the job category based on resume content."""
    categories = {
        "Data Science / AI": ["machine learning", "deep learning", "data analysis", "python", "nlp", "tensorflow", "pytorch", "data scientist"],
        "Software Engineering": ["react", "node", "django", "java", "c++", "software development", "api", "microservices"],
        "Web Development": ["html", "css", "javascript", "frontend", "backend", "fullstack"],
        "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "jenkins"],
        "Product / Project Management": ["agile", "scrum", "jira", "product management", "leadership", "stakeholder"]
    }
    
    text = text.lower()
    scores = {cat: 0 for cat in categories}
    for cat, keywords in categories.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                scores[cat] += 1
                
    best_cat = max(scores, key=scores.get)
    if scores[best_cat] == 0:
        return "General IT / Business"
    return best_cat

def get_resume_suggestions(resume_text):
    """Provides AI-like suggestions to improve the resume."""
    suggestions = []
    text_lower = resume_text.lower()
    words = text_lower.split()
    
    if len(words) < 200:
        suggestions.append("⚠️ **Length:** Your resume is quite short. Consider adding more detail to your experience or projects.")
    elif len(words) > 1000:
        suggestions.append("⚠️ **Length:** Your resume is a bit long. Try to keep it concise and relevant to the job (ideally 1-2 pages).")
        
    if not re.search(r'\b(led|managed|achieved|improved|increased|developed|architected)\b', text_lower):
        suggestions.append("🚀 **Action Verbs:** Use more strong action verbs (e.g., achieved, developed, led) to describe your impact.")
        
    if not re.search(r'\d+%|\d+ \w+', text_lower):
        suggestions.append("📊 **Metrics:** Include more quantifiable metrics (numbers, percentages) to demonstrate tangible results.")
        
    if not re.search(r'\b(education|degree|university|college)\b', text_lower):
        suggestions.append("🎓 **Structure:** Ensure you have a clearly labeled 'Education' section.")
        
    if not suggestions:
        suggestions.append("✅ **Structure:** Your resume looks well-structured! Focus on tailoring keywords to specific job descriptions.")
        
    return suggestions

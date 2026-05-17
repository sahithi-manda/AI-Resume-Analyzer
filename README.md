# AI Resume Analyzer 📄🚀

A comprehensive, AI-powered web application built with Python and Streamlit to analyze resumes, extract skills, calculate ATS (Applicant Tracking System) compatibility, and provide actionable feedback.

## Features ✨

- **PDF Resume Upload:** Easily upload your resume in PDF format.
- **NLP Skill Extraction:** Automatically detects technical and soft skills using Natural Language Processing (spaCy).
- **ATS Score System:** Calculates an ATS compatibility score based on content length, sections, and exact job description matching.
- **Job Description Matching:** Compare your resume directly against a job description to find out match percentage and missing keywords.
- **AI Suggestions:** Receive smart, actionable suggestions to improve your resume structure, action verbs, and metrics.
- **Job Category Prediction:** Automatically predicts the most suitable job role based on your resume content.
- **Modern Dashboard UI:** A clean, responsive, and beautiful interface with dark mode, interactive charts, and animations.
- **Downloadable Report:** Export your resume analysis as a JSON report.

## Tech Stack 🛠️

- **Frontend:** Streamlit, Plotly
- **Backend/Logic:** Python
- **NLP & Text Processing:** spaCy, scikit-learn (TF-IDF Vectorizer), PyPDF2
- **Data Handling:** Pandas, NumPy

## Project Structure 📁

```
AI Resume Analyzer/
│
├── app.py                     # Main Streamlit application
├── utils.py                   # Utility functions for NLP, ATS scoring, and logic
├── requirements.txt           # Python dependencies
├── skills.csv                 # Dataset containing technical and soft skills
├── generate_sample_pdf.py     # Script to generate a dummy PDF resume for testing
├── README.md                  # Project documentation
└── assets/
    ├── sample_job_description.txt # Sample JD for testing
    └── sample_resume.pdf          # Sample resume for testing (generate using script)
```

## Installation & Setup 🚀

1. **Clone the repository or navigate to the project directory:**
   ```bash
   cd "AI Resume Analyzer"
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the spaCy NLP model:**
   The application attempts to do this automatically, but you can install it manually:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Generate a Sample Resume (Optional):**
   If you want a sample resume to test the app, run the generation script:
   ```bash
   python generate_sample_pdf.py
   ```

6. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

## Usage Guide 💡

1. Open the app in your browser (typically `http://localhost:8501`).
2. **Upload** your PDF resume in the left column.
3. (Optional) **Paste a Job Description** in the right column to see how well you match the role.
4. View your **ATS Score** and predicted role on the dashboard.
5. Explore the tabs to see:
   - Match Score & Missing Keywords
   - Extracted Technical/Soft Skills
   - AI Suggestions for Improvement
6. Click **Download Analysis Report** to save your results.

## Contributing 🤝

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## License 📝

This project is licensed under the MIT License.

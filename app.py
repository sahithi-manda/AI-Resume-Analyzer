import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from io import BytesIO
import utils

# Set page config
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# Custom CSS for modern UI and dark mode styling
st.markdown("""
<style>
    /* Global Styles */
    body {
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8f9fa !important;
        font-weight: 600 !important;
    }
    
    /* Highlight Skills */
    .skill-badge {
        display: inline-block;
        padding: 6px 12px;
        margin: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .missing-skill-badge {
        display: inline-block;
        padding: 6px 12px;
        margin: 4px;
        background: linear-gradient(135deg, #ff6b6b 0%, #c0392b 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.8s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

def create_gauge_chart(score, title):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "rgba(118, 75, 162, 1)" if score >= 70 else "rgba(255, 153, 0, 1)" if score >= 40 else "rgba(255, 107, 107, 1)"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': "rgba(255, 107, 107, 0.3)"},
                {'range': [40, 70], 'color': "rgba(255, 153, 0, 0.3)"},
                {'range': [70, 100], 'color': "rgba(102, 126, 234, 0.3)"}],
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=300)
    return fig

# App Header
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;' class='fade-in'>🚀 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0aec0; margin-bottom: 40px;' class='fade-in'>Optimize your resume for ATS and get actionable AI-driven feedback.</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=100)
    st.markdown("### Configuration")
    st.markdown("Upload your resume and optional job description to get a detailed analysis.")
    st.divider()
    st.markdown("### Features")
    st.markdown("- 📝 PDF Parsing\n- 🧠 NLP Skill Extraction\n- 🎯 ATS Scoring\n- 💼 JD Matching\n- 💡 AI Suggestions")
    
# Main Content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 1️⃣ Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

with col2:
    st.markdown("### 2️⃣ Job Description (Optional)")
    job_description = st.text_area("Paste the job description here for ATS matching", height=150)

if uploaded_file is not None:
    with st.spinner("Analyzing your resume with AI..."):
        # Process Resume
        resume_text = utils.extract_text_from_pdf(uploaded_file)
        
        if not resume_text.strip():
            st.error("Could not extract text from the PDF. It might be scanned or image-based.")
        else:
            # Analysis
            skills = utils.extract_skills(resume_text)
            ats_score = utils.calculate_ats_score(resume_text, job_description)
            category = utils.utils.predict_category(resume_text) if hasattr(utils, 'predict_category') else utils.predict_category(resume_text)
            suggestions = utils.get_resume_suggestions(resume_text)
            
            # Dashboard UI
            st.divider()
            st.markdown("<h2 class='fade-in'>📊 Analysis Dashboard</h2>", unsafe_allow_html=True)
            
            # Top Metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"<div class='metric-card'><h3>ATS Score</h3><h2 style='color: {'#667eea' if ats_score>=70 else '#ff9900'};'>{ats_score}%</h2></div>", unsafe_allow_html=True)
            with m2:
                st.markdown(f"<div class='metric-card'><h3>Skills Found</h3><h2>{len(skills)}</h2></div>", unsafe_allow_html=True)
            with m3:
                st.markdown(f"<div class='metric-card'><h3>Predicted Role</h3><h3 style='color: #a0aec0;'>{category}</h3></div>", unsafe_allow_html=True)
            
            # Tabs for detailed view
            tab1, tab2, tab3 = st.tabs(["🎯 Match & Score", "🧠 Extracted Skills", "💡 AI Suggestions"])
            
            with tab1:
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.plotly_chart(create_gauge_chart(ats_score, "ATS Match Score"), use_container_width=True)
                with c2:
                    st.markdown("### Score Breakdown")
                    if ats_score >= 80:
                        st.success("Excellent! Your resume is highly compatible.")
                    elif ats_score >= 50:
                        st.warning("Good, but needs improvement. Review missing keywords.")
                    else:
                        st.error("Low compatibility. Consider restructuring and adding relevant keywords.")
                    
                    if job_description:
                        st.markdown("#### Missing Keywords (from JD)")
                        missing_skills = utils.get_missing_keywords(skills, job_description)
                        if missing_skills:
                            html_missing = "".join([f"<span class='missing-skill-badge'>{s}</span>" for s in missing_skills])
                            st.markdown(html_missing, unsafe_allow_html=True)
                        else:
                            st.success("Great job! You have all the key skills mentioned in the JD.")
                            
            with tab2:
                st.markdown("### Detected Technical & Soft Skills")
                if skills:
                    html_skills = "".join([f"<span class='skill-badge'>{s}</span>" for s in skills])
                    st.markdown(html_skills, unsafe_allow_html=True)
                else:
                    st.info("No predefined skills detected. Check your spelling or add more technical terms.")
                    
            with tab3:
                st.markdown("### AI Suggestions for Improvement")
                for sug in suggestions:
                    st.markdown(f"- {sug}")
                    
            # Export Report
            st.divider()
            st.markdown("### 📥 Export Report")
            report_dict = {
                "Filename": uploaded_file.name,
                "ATS Score": ats_score,
                "Category": category,
                "Skills": skills,
                "Suggestions": suggestions
            }
            if job_description:
                report_dict["Missing Skills from JD"] = missing_skills
                
            report_json = json.dumps(report_dict, indent=4)
            st.download_button(
                label="Download Analysis Report (JSON)",
                data=report_json,
                file_name="resume_analysis_report.json",
                mime="application/json"
            )
else:
    st.info("Please upload a PDF resume to view the analysis dashboard.")
    
# Footer
st.markdown("<br><hr><center><p style='color: gray;'>Built with ❤️ using Streamlit & Python</p></center>", unsafe_allow_html=True)

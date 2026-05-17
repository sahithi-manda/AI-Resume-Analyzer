from fpdf import FPDF
import os

def create_sample_resume():
    if not os.path.exists('assets'):
        os.makedirs('assets')
        
    pdf = FPDF()
    pdf.add_page()
    
    # Fonts
    pdf.set_font("Arial", 'B', 16)
    
    # Header
    pdf.cell(200, 10, txt="John Doe", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt="johndoe@email.com | (123) 456-7890 | github.com/johndoe | linkedin.com/in/johndoe", ln=1, align='C')
    
    pdf.ln(5)
    
    # Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Professional Summary", ln=1, align='L')
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, txt="Dedicated and innovative Software Engineer with 4+ years of experience in full-stack development, machine learning, and cloud infrastructure. Proven ability to design and optimize scalable web applications and integrate AI-driven features. Adept at collaborating with cross-functional teams to deliver high-quality software solutions on time.")
    
    pdf.ln(5)
    
    # Skills
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Technical Skills", ln=1, align='L')
    pdf.set_font("Arial", '', 12)
    skills = "Programming: Python, JavaScript, Java, SQL, C++\n" \
             "Frameworks: React, Node.js, Django, Flask, FastAPI\n" \
             "Machine Learning: Scikit-learn, TensorFlow, Pandas, NumPy\n" \
             "Tools & Cloud: Git, Docker, Kubernetes, AWS, PostgreSQL"
    pdf.multi_cell(0, 8, txt=skills)
    
    pdf.ln(5)
    
    # Experience
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Professional Experience", ln=1, align='L')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, txt="Senior Software Engineer | Tech Innovators Inc. | Jan 2021 - Present", ln=1, align='L')
    pdf.set_font("Arial", '', 12)
    exp1 = "- Developed and maintained robust RESTful APIs using Django and FastAPI, serving over 100K daily requests.\n" \
           "- Architected a scalable microservices infrastructure using Docker and Kubernetes on AWS, reducing deployment time by 40%.\n" \
           "- Implemented a machine learning pipeline using Python and Scikit-learn for customer churn prediction, achieving 85% accuracy.\n" \
           "- Led a team of 4 junior developers, conducting code reviews and mentoring in agile methodologies."
    pdf.multi_cell(0, 8, txt=exp1)
    
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, txt="Software Developer | Web Solutions LLC | Jun 2018 - Dec 2020", ln=1, align='L')
    pdf.set_font("Arial", '', 12)
    exp2 = "- Built dynamic and responsive front-end interfaces using React and Redux.\n" \
           "- Optimized database queries in PostgreSQL, improving application performance and page load speed by 30%.\n" \
           "- Collaborated with UI/UX designers to implement modern design systems."
    pdf.multi_cell(0, 8, txt=exp2)
    
    pdf.ln(5)
    
    # Education
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Education", ln=1, align='L')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, txt="Bachelor of Science in Computer Science | State University | 2014 - 2018", ln=1, align='L')
    
    pdf.output("assets/sample_resume.pdf")
    print("Sample resume generated at assets/sample_resume.pdf")

if __name__ == "__main__":
    create_sample_resume()

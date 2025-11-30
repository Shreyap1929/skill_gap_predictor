import os
import json
import uuid
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

import fitz  
import pdfplumber
import re
import string
from collections import Counter
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import pandas as pd
import requests
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from textdistance import jaro_winkler
from fuzzywuzzy import fuzz, process

load_dotenv()

app = FastAPI(
    title="Skill Gap Predictor API",
    description="API for analyzing university syllabi and identifying skill gaps",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception as e:
    print(f"NLTK download warning: {e}")

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model 'en_core_web_sm' not found. Using basic text processing.")
    nlp = None

DATABASE_PATH = Path(__file__).parent / "database" / "skill_predictor.db"
DATABASE_PATH.parent.mkdir(exist_ok=True)


class SkillAnalysis(BaseModel):
    """Model for skill analysis results"""
    analysis_id: str
    university: str
    field: str
    covered_skills: List[str]
    missing_skills: List[str]
    skill_coverage_percentage: float
    recommendations: List[Dict[str, str]]
    created_at: str


class AnalysisRequest(BaseModel):
    """Model for analysis request"""
    university: str
    field: str
    text_content: Optional[str] = None


def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            university TEXT NOT NULL,
            field TEXT NOT NULL,
            covered_skills TEXT NOT NULL,
            missing_skills TEXT NOT NULL,
            skill_coverage_percentage REAL NOT NULL,
            recommendations TEXT NOT NULL,
            syllabus_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS industry_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            category TEXT NOT NULL,
            importance_level INTEGER NOT NULL,
            source TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF using PyMuPDF and pdfplumber"""
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        if text.strip():
            return text
            
    except Exception as e:
        print(f"PyMuPDF failed: {e}")
    
    try:
        import io
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
        
    except Exception as e:
        print(f"pdfplumber failed: {e}")
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")


def extract_skills_with_nlp(syllabus_text: str, field: str) -> List[str]:
    """Extract skills from syllabus text using NLP techniques (free alternative to LLM)"""
    try:
        skill_database = {
            "Computer Science": [
                "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "Go", "Rust", "Swift", "Kotlin",
                "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express", "Django", "Flask", "Spring",
                "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",
                "Git", "GitHub", "GitLab", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "DevOps", "CI/CD",
                "Machine Learning", "Deep Learning", "Neural Networks", "TensorFlow", "PyTorch", "Scikit-learn",
                "Data Structures", "Algorithms", "Object Oriented Programming", "Functional Programming",
                "API Development", "RESTful APIs", "GraphQL", "Microservices", "System Design", "Software Architecture",
                "Testing", "Unit Testing", "Integration Testing", "Agile", "Scrum", "Linux", "Unix", "Shell Scripting",
                "Web Development", "Frontend Development", "Backend Development", "Full Stack Development",
                "Database Design", "Data Modeling", "Cybersecurity", "Network Security", "Encryption"
            ],
            "Engineering": [
                "MATLAB", "Simulink", "AutoCAD", "SolidWorks", "CATIA", "Inventor", "Fusion 360",
                "CAD", "CAM", "CAE", "FEA", "CFD", "Finite Element Analysis", "Computational Fluid Dynamics",
                "Project Management", "Lean Manufacturing", "Six Sigma", "Quality Control", "Quality Assurance",
                "Statistics", "Linear Algebra", "Calculus", "Differential Equations", "Physics", "Thermodynamics",
                "Materials Science", "Mechanical Design", "Electrical Engineering", "Control Systems",
                "PLC Programming", "SCADA", "HMI", "Industrial Automation", "Robotics", "Mechatronics",
                "3D Modeling", "3D Printing", "Additive Manufacturing", "Manufacturing Processes",
                "Technical Drawing", "Blueprint Reading", "GD&T", "Tolerance Analysis", "Stress Analysis"
            ],
            "Information Technology": [
                "Network Administration", "System Administration", "Cloud Computing", "Virtualization",
                "Windows Server", "Linux Administration", "Active Directory", "LDAP", "DNS", "DHCP",
                "TCP/IP", "Networking", "Routing", "Switching", "Firewalls", "VPN", "VLAN",
                "Cybersecurity", "Information Security", "Risk Assessment", "Compliance", "ITIL", "ITSM",
                "Help Desk", "Technical Support", "Troubleshooting", "Hardware", "Software Installation",
                "Backup and Recovery", "Disaster Recovery", "Business Continuity", "Monitoring", "Performance Tuning",
                "Database Administration", "SQL Server", "Oracle", "MySQL", "PostgreSQL", "MongoDB",
                "PowerShell", "Bash", "Python", "Scripting", "Automation", "Configuration Management"
            ],
            "Electronics": [
                "Circuit Design", "PCB Design", "Analog Electronics", "Digital Electronics", "Power Electronics",
                "Microcontrollers", "Microprocessors", "Embedded Systems", "FPGA", "VHDL", "Verilog",
                "Signal Processing", "Digital Signal Processing", "Image Processing", "Communication Systems",
                "RF Design", "Antenna Design", "Wireless Communication", "Bluetooth", "WiFi", "5G",
                "Arduino", "Raspberry Pi", "PIC", "ARM", "AVR", "STM32", "ESP32",
                "VLSI Design", "ASIC Design", "Semiconductor Physics", "Electronic Measurements",
                "Oscilloscope", "Multimeter", "Function Generator", "Logic Analyzer", "Spectrum Analyzer",
                "Soldering", "PCB Layout", "Schematic Design", "SPICE Simulation", "MATLAB", "LabVIEW"
            ],
            "Artificial Intelligence and Data Science": [
                "Python", "R", "SQL", "Scala", "Julia", "Java", "C++",
                "Machine Learning", "Deep Learning", "Neural Networks", "Artificial Intelligence",
                "Statistics", "Probability", "Linear Algebra", "Calculus", "Statistical Analysis",
                "Data Science", "Data Analysis", "Data Mining", "Data Visualization", "Exploratory Data Analysis",
                "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly", "Bokeh",
                "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "XGBoost", "LightGBM", "CatBoost",
                "Natural Language Processing", "Computer Vision", "Time Series Analysis", "Forecasting",
                "Big Data", "Apache Spark", "Hadoop", "MapReduce", "Hive", "Pig", "Apache Kafka",
                "Tableau", "Power BI", "Jupyter Notebook", "Google Colab", "Apache Airflow",
                "Feature Engineering", "Model Selection", "Cross Validation", "Hyperparameter Tuning",
                "A/B Testing", "Experimental Design", "Causal Inference", "Bayesian Statistics"
            ],
            "Artificial Intelligence and Machine Learning": [
                "Python", "R", "MATLAB", "C++", "Java", "Scala",
                "Machine Learning", "Deep Learning", "Neural Networks", "Artificial Intelligence",
                "Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Transfer Learning",
                "Convolutional Neural Networks", "Recurrent Neural Networks", "LSTM", "GRU", "Transformers",
                "Computer Vision", "Natural Language Processing", "Speech Recognition", "Robotics",
                "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "OpenCV", "NLTK", "spaCy", "Hugging Face",
                "Linear Algebra", "Calculus", "Statistics", "Probability", "Optimization", "Information Theory",
                "Feature Engineering", "Dimensionality Reduction", "PCA", "t-SNE", "UMAP",
                "Model Evaluation", "Cross Validation", "Bias-Variance Tradeoff", "Regularization",
                "Ensemble Methods", "Random Forest", "Gradient Boosting", "XGBoost", "AdaBoost",
                "Neural Architecture Search", "AutoML", "MLOps", "Model Deployment", "Edge AI",
                "Ethics in AI", "Fairness", "Interpretability", "Explainable AI", "Adversarial Examples"
            ]
        }

        relevant_skills = skill_database.get(field, skill_database["Computer Science"])

        text_clean = clean_text_for_skill_extraction(syllabus_text)

        extracted_skills = set()
 
        extracted_skills.update(extract_skills_keyword_matching(text_clean, relevant_skills))

        if nlp:
            extracted_skills.update(extract_skills_with_spacy(text_clean, relevant_skills))
  
        extracted_skills.update(extract_skills_pattern_matching(text_clean))
  
        extracted_skills.update(extract_skills_context_based(text_clean, relevant_skills))
  
        final_skills = rank_and_filter_skills(list(extracted_skills), relevant_skills, text_clean)
        
        return final_skills[:25]  
        
    except Exception as e:
        print(f"NLP extraction failed: {e}")
        return extract_skills_basic(syllabus_text)


def clean_text_for_skill_extraction(text: str) -> str:
    """Clean and preprocess text for better skill extraction"""
    text = text.lower()

    text = re.sub(r'[^\w\s\+\#\.\-]', ' ', text)
    
    replacements = {
        'javascript': 'JavaScript',
        'typescript': 'TypeScript',
        'c++': 'C++',
        'c#': 'C#',
        'node.js': 'Node.js',
        'vue.js': 'Vue.js',
        'asp.net': 'ASP.NET',
        'sql server': 'SQL Server',
        'mysql': 'MySQL',
        'postgresql': 'PostgreSQL',
        'mongodb': 'MongoDB'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def extract_skills_keyword_matching(text: str, relevant_skills: List[str]) -> List[str]:
    """Extract skills using fuzzy keyword matching"""
    found_skills = []
    text_words = set(text.lower().split())
    
    for skill in relevant_skills:
        skill_lower = skill.lower()
        
        if skill_lower in text.lower():
            found_skills.append(skill)
            continue

        skill_words = skill_lower.split()
        
        if len(skill_words) == 1:
            
            matches = process.extractOne(skill_lower, text_words, scorer=fuzz.ratio)
            if matches and matches[1] > 85:  
                found_skills.append(skill)
        else:
           
            if all(word in text_words for word in skill_words):
                found_skills.append(skill)
    
    return found_skills


def extract_skills_with_spacy(text: str, relevant_skills: List[str]) -> List[str]:
    """Extract skills using spaCy NLP processing"""
    if not nlp:
        return []
    
    doc = nlp(text)
    found_skills = []
    
    entities = [ent.text.strip() for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']]

    noun_phrases = [chunk.text.strip() for chunk in doc.noun_chunks]

    candidates = set(entities + noun_phrases)
    
    for candidate in candidates:
        matches = process.extractOne(candidate.lower(), [skill.lower() for skill in relevant_skills])
        if matches and matches[1] > 80:
            
            for skill in relevant_skills:
                if skill.lower() == matches[0]:
                    found_skills.append(skill)
                    break
    
    return found_skills


def extract_skills_pattern_matching(text: str) -> List[str]:
    """Extract skills using pattern matching for technical terms"""
    found_skills = []
    
    patterns = {
        'Programming Languages': [
            r'\b(python|java|javascript|typescript|c\+\+|c#|go|rust|swift|kotlin|php|ruby|scala|r\b)\b',
            r'\b(html|css|sql|nosql|xml|json|yaml)\b'
        ],
        'Frameworks and Libraries': [
            r'\b(react|angular|vue\.?js|node\.?js|express|django|flask|spring|laravel)\b',
            r'\b(tensorflow|pytorch|keras|scikit-learn|pandas|numpy|opencv)\b'
        ],
        'Tools and Platforms': [
            r'\b(git|github|gitlab|docker|kubernetes|aws|azure|gcp|jenkins)\b',
            r'\b(matlab|autocad|solidworks|tableau|power\s?bi)\b'
        ],
        'Databases': [
            r'\b(mysql|postgresql|mongodb|redis|elasticsearch|oracle|sql\s?server)\b'
        ],
        'Concepts': [
            r'\b(machine\s?learning|deep\s?learning|neural\s?networks|api|microservices)\b',
            r'\b(devops|agile|scrum|ci/cd|version\s?control)\b'
        ]
    }
    
    for category, pattern_list in patterns.items():
        for pattern in pattern_list:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                
                skill = match.replace('_', ' ').title()
                if skill not in found_skills:
                    found_skills.append(skill)
    
    return found_skills


def extract_skills_context_based(text: str, relevant_skills: List[str]) -> List[str]:
    """Extract skills based on context indicators"""
    found_skills = []
    
    context_patterns = [
        r'(?:learn|study|course|subject|module|lab|practical|theory|programming|development|design|analysis|using|with|in)\s+([A-Za-z\+\#\.]+)',
        r'([A-Za-z\+\#\.]+)\s+(?:programming|language|framework|library|tool|software|platform|database|system)',
        r'(?:introduction to|fundamentals of|advanced|basic)\s+([A-Za-z\+\#\.]+)',
        r'([A-Za-z\+\#\.]+)\s+(?:concepts|principles|methodology|techniques|algorithms)'
    ]
    
    for pattern in context_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            
            skill_candidate = match.strip().title()
            
            closest_match = process.extractOne(skill_candidate.lower(), [skill.lower() for skill in relevant_skills])
            if closest_match and closest_match[1] > 75:
                
                for skill in relevant_skills:
                    if skill.lower() == closest_match[0] and skill not in found_skills:
                        found_skills.append(skill)
                        break
    
    return found_skills


def rank_and_filter_skills(extracted_skills: List[str], relevant_skills: List[str], text: str) -> List[str]:
    """Rank and filter extracted skills based on relevance and frequency"""
    if not extracted_skills:
        return []
    
    skill_scores = {}
    
    for skill in extracted_skills:
        score = 0
        skill_lower = skill.lower()
        
        score += text.lower().count(skill_lower) * 2
        
        if skill in relevant_skills:
            score += 5
        
        if len(skill) < 3:
            score -= 2
        
        if any(char in skill for char in ['.', '+', '#', '-']):
            score += 3
        
        skill_scores[skill] = score
    
    
    ranked_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
    return [skill for skill, score in ranked_skills if score > 0]


def extract_skills_basic(text: str) -> List[str]:
    """Basic keyword-based skill extraction as fallback"""
    common_skills = [
        "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "React", "Angular",
        "Machine Learning", "Data Science", "Statistics", "Linear Algebra", "Calculus",
        "Data Structures", "Algorithms", "Database Management", "Web Development",
        "Software Engineering", "Object Oriented Programming", "Git", "Linux",
        "Cloud Computing", "Docker", "Kubernetes", "AWS", "MongoDB", "PostgreSQL"
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills[:15]  


def get_industry_skills(field: str) -> List[str]:
    """Get industry-required skills for a given field"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT skill_name FROM industry_skills 
        WHERE field = ? OR field = 'General'
        ORDER BY importance_level DESC
    """, (field,))
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        return [row[0] for row in results]
    
    default_skills = {
        "Computer Science": [
            "Python", "Java", "C++", "JavaScript", "SQL", "Data Structures", "Algorithms",
            "Machine Learning", "Web Development", "Database Management", "Git", "Linux",
            "Cloud Computing", "Docker", "API Development", "System Design", "DevOps",
            "React", "Node.js", "MongoDB", "PostgreSQL", "AWS", "Kubernetes"
        ],
        "Engineering": [
            "MATLAB", "AutoCAD", "SolidWorks", "Project Management", "Statistics",
            "Linear Algebra", "Calculus", "Physics", "Python", "R", "Data Analysis",
            "Quality Control", "Lean Manufacturing", "Six Sigma", "CAD", "FEA"
        ],
        "Information Technology": [
            "Network Administration", "Cybersecurity", "Cloud Computing", "System Administration",
            "Help Desk Support", "Database Administration", "Windows Server", "Linux Administration",
            "Virtualization", "Backup and Recovery", "IT Support", "Network Security"
        ],
        "Electronics": [
            "Circuit Design", "VLSI Design", "Embedded Systems", "Microcontrollers", "PCB Design",
            "Signal Processing", "FPGA Programming", "Arduino", "Raspberry Pi", "Electronics Design",
            "Digital Signal Processing", "Analog Electronics", "Power Electronics"
        ],
        "Artificial Intelligence and Data Science": [
            "Python", "Machine Learning", "Deep Learning", "Data Science", "Statistics", "R",
            "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn", "SQL", "Data Visualization",
            "Natural Language Processing", "Computer Vision", "Big Data", "Apache Spark", "Hadoop",
            "Tableau", "Power BI", "Statistical Analysis", "Neural Networks"
        ],
        "Artificial Intelligence and Machine Learning": [
            "Python", "Machine Learning", "Deep Learning", "Neural Networks", "TensorFlow", "PyTorch",
            "Scikit-learn", "Computer Vision", "Natural Language Processing", "Reinforcement Learning",
            "Statistics", "Linear Algebra", "Calculus", "Data Preprocessing", "Model Evaluation",
            "Feature Engineering", "Hyperparameter Tuning", "MLOps", "AI Ethics", "Keras", "OpenCV"
        ]
    }
    
    return default_skills.get(field, default_skills["Computer Science"])


def compare_skills(covered_skills: List[str], industry_skills: List[str]) -> Dict[str, Any]:
    """Compare covered skills with industry requirements"""
    covered_set = set(skill.lower() for skill in covered_skills)
    industry_set = set(skill.lower() for skill in industry_skills)
    
    
    missing_lower = industry_set - covered_set
    missing_skills = [skill for skill in industry_skills if skill.lower() in missing_lower]
    
    if industry_skills:
        coverage_percentage = len(covered_set.intersection(industry_set)) / len(industry_set) * 100
    else:
        coverage_percentage = 0
    
    return {
        "missing_skills": missing_skills,
        "coverage_percentage": round(coverage_percentage, 2)
    }


def generate_recommendations(missing_skills: List[str]) -> List[Dict[str, str]]:
    """Generate learning recommendations for missing skills"""
    recommendations = []
    
    learning_platforms = {
        "Python": {
            "title": "Python Programming Complete Course",
            "platform": "Coursera",
            "url": "https://coursera.org/learn/python",
            "description": "Learn Python from basics to advanced concepts"
        },
        "Machine Learning": {
            "title": "Machine Learning Specialization",
            "platform": "Coursera",
            "url": "https://coursera.org/specializations/machine-learning",
            "description": "Comprehensive ML course by Andrew Ng"
        },
        "JavaScript": {
            "title": "The Complete JavaScript Course",
            "platform": "Udemy",
            "url": "https://udemy.com/course/the-complete-javascript-course",
            "description": "Master JavaScript with projects and real-world applications"
        },
        "React": {
            "title": "React - The Complete Guide",
            "platform": "Udemy",
            "url": "https://udemy.com/course/react-the-complete-guide",
            "description": "Learn React.js from scratch with hooks and modern patterns"
        },
        "SQL": {
            "title": "SQL for Data Science",
            "platform": "Coursera",
            "url": "https://coursera.org/learn/sql-for-data-science",
            "description": "Master SQL for data analysis and database management"
        }
    }
    
    for skill in missing_skills[:10]: 
        if skill in learning_platforms:
            recommendations.append(learning_platforms[skill])
        else:
            recommendations.append({
                "title": f"Learn {skill}",
                "platform": "Search Multiple Platforms",
                "url": f"https://www.google.com/search?q=learn+{skill.replace(' ', '+')}+online+course",
                "description": f"Find comprehensive courses for {skill} on various platforms"
            })
    
    return recommendations


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_database()
    populate_sample_skills()


def populate_sample_skills():
    """Populate database with sample industry skills"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT COUNT(*) FROM industry_skills")
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_skills = [
            
            ("Computer Science", "Python", "Programming", 10, "Industry Survey"),
            ("Computer Science", "Java", "Programming", 9, "Industry Survey"),
            ("Computer Science", "JavaScript", "Programming", 9, "Industry Survey"),
            ("Computer Science", "SQL", "Database", 10, "Industry Survey"),
            ("Computer Science", "React", "Frontend", 8, "Industry Survey"),
            ("Computer Science", "Node.js", "Backend", 8, "Industry Survey"),
            ("Computer Science", "Git", "Version Control", 10, "Industry Survey"),
            ("Computer Science", "Docker", "DevOps", 7, "Industry Survey"),
            ("Computer Science", "AWS", "Cloud", 8, "Industry Survey"),
            ("Computer Science", "Machine Learning", "AI/ML", 9, "Industry Survey"),
            ("Computer Science", "Data Structures", "Fundamentals", 10, "Industry Survey"),
            ("Computer Science", "Algorithms", "Fundamentals", 10, "Industry Survey"),
            
            
            ("Engineering", "MATLAB", "Analysis", 8, "Industry Survey"),
            ("Engineering", "AutoCAD", "Design", 7, "Industry Survey"),
            ("Engineering", "Project Management", "Management", 9, "Industry Survey"),
            ("Engineering", "Statistics", "Analysis", 8, "Industry Survey"),
            ("Engineering", "Python", "Programming", 7, "Industry Survey"),
            

            ("Data Science", "Python", "Programming", 10, "Industry Survey"),
            ("Data Science", "R", "Programming", 8, "Industry Survey"),
            ("Data Science", "SQL", "Database", 10, "Industry Survey"),
            ("Data Science", "Machine Learning", "ML", 10, "Industry Survey"),
            ("Data Science", "Statistics", "Mathematics", 10, "Industry Survey"),
            ("Data Science", "Pandas", "Data Processing", 9, "Industry Survey"),
            ("Data Science", "NumPy", "Data Processing", 9, "Industry Survey"),
            ("Data Science", "Tableau", "Visualization", 8, "Industry Survey"),
        ]
        
        cursor.executemany(
            "INSERT INTO industry_skills (field, skill_name, category, importance_level, source) VALUES (?, ?, ?, ?, ?)",
            sample_skills
        )
        
        conn.commit()
    
    conn.close()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Skill Gap Predictor API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/analyze", response_model=SkillAnalysis)
async def analyze_syllabus(
    file: UploadFile = File(None),
    university: str = Form(...),
    field: str = Form(...),
    text_content: str = Form(None)
):
    """
    Analyze uploaded syllabus or text content for skill gaps
    """
    try:
        analysis_id = str(uuid.uuid4())
        
        if file:
            if file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="Only PDF files are supported")
            
            file_content = await file.read()
            syllabus_text = extract_text_from_pdf(file_content)
        elif text_content:
            syllabus_text = text_content
        else:
            raise HTTPException(status_code=400, detail="Either file or text_content must be provided")
        
        if not syllabus_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in the provided input")
        
        covered_skills = extract_skills_with_nlp(syllabus_text, field)
        
        industry_skills = get_industry_skills(field)
        
        comparison = compare_skills(covered_skills, industry_skills)
        
        recommendations = generate_recommendations(comparison["missing_skills"])
        
        analysis = SkillAnalysis(
            analysis_id=analysis_id,
            university=university,
            field=field,
            covered_skills=covered_skills,
            missing_skills=comparison["missing_skills"],
            skill_coverage_percentage=comparison["coverage_percentage"],
            recommendations=recommendations,
            created_at=datetime.now().isoformat()
        )
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analyses 
            (id, university, field, covered_skills, missing_skills, skill_coverage_percentage, recommendations, syllabus_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis_id,
            university,
            field,
            json.dumps(covered_skills),
            json.dumps(comparison["missing_skills"]),
            comparison["coverage_percentage"],
            json.dumps(recommendations),
            syllabus_text[:5000]  
        ))
        
        conn.commit()
        conn.close()
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/skills/{analysis_id}", response_model=SkillAnalysis)
async def get_analysis(analysis_id: str):
    """
    Retrieve a previous skill gap analysis by ID
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, university, field, covered_skills, missing_skills, 
                   skill_coverage_percentage, recommendations, created_at
            FROM analyses 
            WHERE id = ?
        """, (analysis_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return SkillAnalysis(
            analysis_id=result[0],
            university=result[1],
            field=result[2],
            covered_skills=json.loads(result[3]),
            missing_skills=json.loads(result[4]),
            skill_coverage_percentage=result[5],
            recommendations=json.loads(result[6]),
            created_at=result[7]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analysis: {str(e)}")


@app.get("/fields")
async def get_available_fields():
    """Get list of available fields for analysis"""
    return {
        "fields": [
            "Engineering",
            "Computer Science",
            "Information Technology",
            "Electronics",
            "Artificial Intelligence and Data Science",
            "Artificial Intelligence and Machine Learning"
        ]
    }


@app.get("/analyses")
async def get_recent_analyses(limit: int = 10):
    """Get recent analyses"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, university, field, skill_coverage_percentage, created_at
            FROM analyses 
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        analyses = []
        for row in results:
            analyses.append({
                "analysis_id": row[0],
                "university": row[1],
                "field": row[2],
                "coverage_percentage": row[3],
                "created_at": row[4]
            })
        
        return {"analyses": analyses}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analyses: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

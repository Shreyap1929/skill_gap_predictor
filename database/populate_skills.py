import sqlite3
import json
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent / "backend" / "database" / "skill_predictor.db"
DATABASE_PATH.parent.mkdir(exist_ok=True)

def create_comprehensive_skills_data():
    """Create comprehensive industry skills dataset"""
    
    skills_data = [
        # Computer Science & Software Engineering
        ("Computer Science", "Python", "Programming Languages", 10, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "JavaScript", "Programming Languages", 10, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "Java", "Programming Languages", 9, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "TypeScript", "Programming Languages", 8, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "C++", "Programming Languages", 7, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "C#", "Programming Languages", 7, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "Go", "Programming Languages", 6, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "Rust", "Programming Languages", 5, "Stack Overflow Developer Survey 2024"),
        
        # Web Development
        ("Computer Science", "React", "Frontend Frameworks", 10, "State of JS 2024"),
        ("Computer Science", "Node.js", "Backend Frameworks", 9, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "Vue.js", "Frontend Frameworks", 7, "State of JS 2024"),
        ("Computer Science", "Angular", "Frontend Frameworks", 6, "State of JS 2024"),
        ("Computer Science", "Express.js", "Backend Frameworks", 8, "NPM Trends 2024"),
        ("Computer Science", "Next.js", "Full-stack Frameworks", 8, "State of JS 2024"),
        ("Computer Science", "HTML", "Web Technologies", 10, "Web Standards"),
        ("Computer Science", "CSS", "Web Technologies", 10, "Web Standards"),
        
        # Database Technologies
        ("Computer Science", "SQL", "Database Technologies", 10, "DB-Engines Ranking 2024"),
        ("Computer Science", "PostgreSQL", "Database Technologies", 9, "DB-Engines Ranking 2024"),
        ("Computer Science", "MongoDB", "Database Technologies", 8, "DB-Engines Ranking 2024"),
        ("Computer Science", "MySQL", "Database Technologies", 8, "DB-Engines Ranking 2024"),
        ("Computer Science", "Redis", "Database Technologies", 7, "DB-Engines Ranking 2024"),
        ("Computer Science", "Elasticsearch", "Database Technologies", 6, "DB-Engines Ranking 2024"),
        
        # Cloud & DevOps
        ("Computer Science", "AWS", "Cloud Platforms", 10, "Cloud Market Share 2024"),
        ("Computer Science", "Docker", "DevOps Tools", 9, "Stack Overflow Developer Survey 2024"),
        ("Computer Science", "Kubernetes", "DevOps Tools", 8, "CNCF Survey 2024"),
        ("Computer Science", "Git", "Version Control", 10, "Git Usage Statistics 2024"),
        ("Computer Science", "CI/CD", "DevOps Practices", 9, "DevOps Report 2024"),
        ("Computer Science", "Azure", "Cloud Platforms", 8, "Cloud Market Share 2024"),
        ("Computer Science", "Google Cloud Platform", "Cloud Platforms", 7, "Cloud Market Share 2024"),
        
        # Fundamental CS Concepts
        ("Computer Science", "Data Structures", "Computer Science Fundamentals", 10, "CS Curriculum Standards"),
        ("Computer Science", "Algorithms", "Computer Science Fundamentals", 10, "CS Curriculum Standards"),
        ("Computer Science", "Object Oriented Programming", "Programming Paradigms", 9, "CS Curriculum Standards"),
        ("Computer Science", "System Design", "Software Architecture", 8, "Tech Interview Trends 2024"),
        ("Computer Science", "Software Engineering", "Development Practices", 9, "ACM Curriculum Guidelines"),
        ("Computer Science", "Computer Networks", "Computer Science Fundamentals", 7, "CS Curriculum Standards"),
        ("Computer Science", "Operating Systems", "Computer Science Fundamentals", 7, "CS Curriculum Standards"),
        ("Computer Science", "Database Management", "Computer Science Fundamentals", 8, "CS Curriculum Standards"),
        
        # Information Technology Skills
        ("Information Technology", "Network Administration", "IT Infrastructure", 10, "IT Skills Survey 2024"),
        ("Information Technology", "Cybersecurity", "Security", 10, "Cybersecurity Skills Gap 2024"),
        ("Information Technology", "Cloud Computing", "Infrastructure", 9, "Cloud Adoption Report 2024"),
        ("Information Technology", "System Administration", "IT Operations", 9, "IT Operations Survey 2024"),
        ("Information Technology", "Windows Server", "Operating Systems", 8, "Windows Server Usage 2024"),
        ("Information Technology", "Linux Administration", "Operating Systems", 8, "Linux Server Survey 2024"),
        ("Information Technology", "Database Administration", "Data Management", 7, "Database Administration Survey 2024"),
        ("Information Technology", "Help Desk Support", "User Support", 7, "IT Support Industry Analysis 2024"),
        ("Information Technology", "Virtualization", "Infrastructure", 8, "Virtualization Trends 2024"),
        ("Information Technology", "Backup and Recovery", "Data Protection", 8, "Data Protection Survey 2024"),
        ("Information Technology", "Network Security", "Security", 9, "Network Security Trends 2024"),
        ("Information Technology", "IT Support", "User Support", 7, "IT Support Skills 2024"),
        
        # Electronics Skills
        ("Electronics", "Circuit Design", "Hardware Design", 10, "Electronics Industry Report 2024"),
        ("Electronics", "VLSI Design", "Hardware Design", 8, "Semiconductor Industry Analysis 2024"),
        ("Electronics", "Embedded Systems", "Hardware/Software", 9, "IoT Market Report 2024"),
        ("Electronics", "Microcontrollers", "Hardware Components", 9, "Embedded Systems Survey 2024"),
        ("Electronics", "PCB Design", "Hardware Design", 8, "Electronics Manufacturing Report 2024"),
        ("Electronics", "Signal Processing", "Analysis Methods", 7, "Signal Processing Applications 2024"),
        ("Electronics", "FPGA Programming", "Hardware Programming", 7, "FPGA Market Analysis 2024"),
        ("Electronics", "Arduino", "Development Platforms", 8, "Maker Movement Survey 2024"),
        ("Electronics", "Raspberry Pi", "Development Platforms", 7, "IoT Development Survey 2024"),
        ("Electronics", "Electronics Design", "Design Methods", 8, "Electronics Design Trends 2024"),
        ("Electronics", "Digital Signal Processing", "Signal Processing", 7, "DSP Applications 2024"),
        ("Electronics", "Analog Electronics", "Circuit Design", 7, "Analog Design Survey 2024"),
        ("Electronics", "Power Electronics", "Power Systems", 6, "Power Electronics Market 2024"),
        
        # AI and Data Science Skills
        ("Artificial Intelligence and Data Science", "Python", "Programming Languages", 10, "AI/DS Survey 2024"),
        ("Artificial Intelligence and Data Science", "Machine Learning", "AI/ML", 10, "AI Job Market Report 2024"),
        ("Artificial Intelligence and Data Science", "Deep Learning", "AI/ML", 9, "Deep Learning Survey 2024"),
        ("Artificial Intelligence and Data Science", "Data Science", "Data Analysis", 10, "Data Science Skills Report 2024"),
        ("Artificial Intelligence and Data Science", "Statistics", "Mathematics", 10, "Statistical Analysis Survey 2024"),
        ("Artificial Intelligence and Data Science", "R", "Programming Languages", 7, "R Usage in Data Science 2024"),
        ("Artificial Intelligence and Data Science", "TensorFlow", "Deep Learning Frameworks", 8, "AI Framework Survey 2024"),
        ("Artificial Intelligence and Data Science", "PyTorch", "Deep Learning Frameworks", 8, "PyTorch Usage 2024"),
        ("Artificial Intelligence and Data Science", "Pandas", "Data Processing", 9, "Python Data Science Survey 2024"),
        ("Artificial Intelligence and Data Science", "NumPy", "Data Processing", 9, "NumPy Usage Survey 2024"),
        ("Artificial Intelligence and Data Science", "Scikit-learn", "Machine Learning Libraries", 8, "ML Library Usage 2024"),
        ("Artificial Intelligence and Data Science", "SQL", "Database Technologies", 9, "SQL in Data Science 2024"),
        ("Artificial Intelligence and Data Science", "Data Visualization", "Visualization", 8, "Data Viz Trends 2024"),
        ("Artificial Intelligence and Data Science", "Natural Language Processing", "AI Specialization", 7, "NLP Market 2024"),
        ("Artificial Intelligence and Data Science", "Computer Vision", "AI Specialization", 7, "Computer Vision Survey 2024"),
        ("Artificial Intelligence and Data Science", "Big Data", "Data Technologies", 7, "Big Data Survey 2024"),
        ("Artificial Intelligence and Data Science", "Apache Spark", "Big Data Technologies", 6, "Spark Usage 2024"),
        ("Artificial Intelligence and Data Science", "Hadoop", "Big Data Technologies", 5, "Hadoop Survey 2024"),
        ("Artificial Intelligence and Data Science", "Tableau", "Data Visualization", 7, "Tableau Usage 2024"),
        ("Artificial Intelligence and Data Science", "Power BI", "Data Visualization", 6, "Power BI Survey 2024"),
        ("Artificial Intelligence and Data Science", "Statistical Analysis", "Statistics", 9, "Statistical Methods 2024"),
        ("Artificial Intelligence and Data Science", "Neural Networks", "Deep Learning", 8, "Neural Network Applications 2024"),
        
        # AI and Machine Learning Skills
        ("Artificial Intelligence and Machine Learning", "Python", "Programming Languages", 10, "AI/ML Programming Survey 2024"),
        ("Artificial Intelligence and Machine Learning", "Machine Learning", "Core ML", 10, "ML Industry Report 2024"),
        ("Artificial Intelligence and Machine Learning", "Deep Learning", "Advanced ML", 10, "Deep Learning Trends 2024"),
        ("Artificial Intelligence and Machine Learning", "Neural Networks", "ML Architectures", 9, "Neural Network Survey 2024"),
        ("Artificial Intelligence and Machine Learning", "TensorFlow", "ML Frameworks", 9, "TensorFlow Usage 2024"),
        ("Artificial Intelligence and Machine Learning", "PyTorch", "ML Frameworks", 9, "PyTorch Adoption 2024"),
        ("Artificial Intelligence and Machine Learning", "Scikit-learn", "ML Libraries", 8, "Scikit-learn Survey 2024"),
        ("Artificial Intelligence and Machine Learning", "Computer Vision", "AI Specialization", 8, "Computer Vision Jobs 2024"),
        ("Artificial Intelligence and Machine Learning", "Natural Language Processing", "AI Specialization", 8, "NLP Applications 2024"),
        ("Artificial Intelligence and Machine Learning", "Reinforcement Learning", "Advanced ML", 7, "RL Applications 2024"),
        ("Artificial Intelligence and Machine Learning", "Statistics", "Mathematics", 9, "Statistics for ML 2024"),
        ("Artificial Intelligence and Machine Learning", "Linear Algebra", "Mathematics", 9, "Math for ML 2024"),
        ("Artificial Intelligence and Machine Learning", "Calculus", "Mathematics", 8, "Calculus in ML 2024"),
        ("Artificial Intelligence and Machine Learning", "Data Preprocessing", "Data Preparation", 8, "Data Preprocessing 2024"),
        ("Artificial Intelligence and Machine Learning", "Model Evaluation", "ML Practices", 8, "Model Evaluation Methods 2024"),
        ("Artificial Intelligence and Machine Learning", "Feature Engineering", "Data Engineering", 7, "Feature Engineering 2024"),
        ("Artificial Intelligence and Machine Learning", "Hyperparameter Tuning", "ML Optimization", 7, "Hyperparameter Methods 2024"),
        ("Artificial Intelligence and Machine Learning", "MLOps", "ML Operations", 7, "MLOps Trends 2024"),
        ("Artificial Intelligence and Machine Learning", "AI Ethics", "Ethics", 6, "AI Ethics Importance 2024"),
        ("Artificial Intelligence and Machine Learning", "Keras", "ML Libraries", 7, "Keras Usage 2024"),
        ("Artificial Intelligence and Machine Learning", "OpenCV", "Computer Vision", 7, "OpenCV Applications 2024"),
        
        # Engineering (General)
        ("Engineering", "MATLAB", "Analysis Software", 8, "Engineering Software Survey 2024"),
        ("Engineering", "Python", "Programming Languages", 7, "Engineering Programming Trends 2024"),
        ("Engineering", "AutoCAD", "Design Software", 7, "CAD Software Market 2024"),
        ("Engineering", "SolidWorks", "Design Software", 6, "CAD Software Market 2024"),
        ("Engineering", "Project Management", "Management Skills", 9, "PMI Industry Report 2024"),
        ("Engineering", "Statistics", "Mathematical Analysis", 8, "Engineering Mathematics Curriculum"),
        ("Engineering", "Linear Algebra", "Mathematical Analysis", 7, "Engineering Mathematics Curriculum"),
        ("Engineering", "Calculus", "Mathematical Analysis", 8, "Engineering Mathematics Curriculum"),
        ("Engineering", "Finite Element Analysis", "Analysis Methods", 6, "Engineering Simulation Market 2024"),
        ("Engineering", "Quality Control", "Process Management", 7, "Quality Management Standards 2024"),
        ("Engineering", "CAD", "Design Tools", 8, "CAD Usage in Engineering 2024"),
        ("Engineering", "FEA", "Analysis Tools", 6, "FEA Software Market 2024"),
        
        # General Skills 
        ("General", "Communication Skills", "Soft Skills", 10, "Employer Skills Survey 2024"),
        ("General", "Problem Solving", "Soft Skills", 10, "Critical Skills Report 2024"),
        ("General", "Teamwork", "Soft Skills", 9, "Workplace Skills Analysis 2024"),
        ("General", "Critical Thinking", "Soft Skills", 9, "21st Century Skills Report"),
        ("General", "Time Management", "Soft Skills", 8, "Productivity Skills Survey 2024"),
        ("General", "Leadership", "Soft Skills", 7, "Leadership Skills Report 2024"),
        ("General", "Adaptability", "Soft Skills", 8, "Future of Work Report 2024"),
        ("General", "Technical Writing", "Communication", 7, "Technical Communication Survey 2024"),
        ("General", "Presentation Skills", "Communication", 7, "Professional Skills Report 2024"),
    ]
    
    return skills_data

def populate_industry_skills():
    """Populate the database with comprehensive industry skills"""

    DATABASE_PATH.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

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
 
    cursor.execute("DELETE FROM industry_skills")

    skills_data = create_comprehensive_skills_data()
    cursor.executemany(
        "INSERT INTO industry_skills (field, skill_name, category, importance_level, source) VALUES (?, ?, ?, ?, ?)",
        skills_data
    )
    
    conn.commit()

    cursor.execute("SELECT field, COUNT(*) FROM industry_skills GROUP BY field ORDER BY COUNT(*) DESC")
    field_stats = cursor.fetchall()
    
    print("Industry skills database populated successfully!")
    print(f"Total skills added: {len(skills_data)}")
    print("\n Skills by field:")
    for field, count in field_stats:
        print(f"  • {field}: {count} skills")

    cursor.execute("""
        SELECT skill_name, field, importance_level 
        FROM industry_skills 
        WHERE importance_level >= 9 
        ORDER BY importance_level DESC, field, skill_name
        LIMIT 20
    """)
    top_skills = cursor.fetchall()
    
    print(f"\nTop {len(top_skills)} most important skills:")
    for skill, field, importance in top_skills:
        print(f"  • {skill} ({field}) - Importance: {importance}/10")
    
    conn.close()

if __name__ == "__main__":
    populate_industry_skills()

# Skill Gap Predictor

A full-stack web application that analyzes university syllabi to identify skill gaps compared to industry requirements.

<img width="1891" height="922" alt="image" src="https://github.com/user-attachments/assets/7a931ac8-2d4b-429e-97ae-6afd9c4244b1" />

# Overview

Upload your syllabus (PDF or text)

<img width="1887" height="917" alt="image" src="https://github.com/user-attachments/assets/c1e20d67-a5a9-42f0-8b80-c412eab709c0" />
<img width="813" height="775" alt="image" src="https://github.com/user-attachments/assets/d57587c2-d33a-4894-ae2d-afafdef51ec8" />


Extract technical skills using AI/NLP
Compare with industry standards

<img width="538" height="886" alt="image" src="https://github.com/user-attachments/assets/c6b9518c-3d80-4d31-b364-b36d3891674b" />

See missing skills and get learning recommendations

![WhatsApp Image 2025-11-30 at 5 40 11 PM](https://github.com/user-attachments/assets/0bb7ffbe-c294-4a38-818c-0d61b22a714c)
![WhatsApp Image 2025-11-30 at 5 40 12 PM](https://github.com/user-attachments/assets/376b5a2f-4ca2-4fb9-bc0f-ebc0c5716262)
![WhatsApp Image 2025-11-30 at 5 40 12 PM (2)](https://github.com/user-attachments/assets/26ab91aa-07d6-4f81-85ad-13ff79169b06)
![WhatsApp Image 2025-11-30 at 5 40 12 PM (1)](https://github.com/user-attachments/assets/54f29334-574d-4c4b-a877-5e206d546328)
![WhatsApp Image 2025-11-30 at 5 40 13 PM](https://github.com/user-attachments/assets/b774a68f-c797-4f93-9b21-ddc120a8a1d4)

# Setup Steps

# Clone repository

git clone https://github.com/Shreyap1929/skill_gap_predictor.git

cd skill_gap_predictor_new


# Backend setup

cd backend

python -m venv venv

Activate venv

Windows: venv\Scripts\activate

Linux/Mac: source venv/bin/activate

pip install -r requirements.txt

python setup_nlp.py

# Initialize database

cd ../database

python populate_skills.py

cd ../backend

# Start backend server

python -m uvicorn main:app --reload

# Frontend setup (new terminal)

cd frontend

npm install

echo "REACT_APP_API_URL=http://localhost:8000" > .env.local

npm start

Access the app at http://localhost:3000

# Features

PDF Processing

Skill Extraction using NLP

Industry skill comparison

Gap analysis with interactive charts

Learning recommendations

# Supported Fields

Computer Science | Data Science | IT | Electronics | Mechanical | Business | Math | Physics

# How It Works

Upload syllabus

Backend extracts and processes text

NLP identifies technical skills

Skills matched against industry database

Gap analysis shown in charts with recommendations

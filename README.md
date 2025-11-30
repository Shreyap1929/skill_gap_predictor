# Skill Gap Predictor

A full-stack web application that analyzes university syllabi to identify skill gaps compared to industry requirements.

# Overview

Upload your syllabus (PDF or text)

Extract technical skills using AI/NLP

Compare with industry standards

See missing skills and get learning recommendations

# Setup Steps

# Clone repository

git clone https://github.com/yourusername/skill-gap-predictor.git
cd skill_gap_predictor_new


# Backend setup

cd backend
python -m venv venv
# Activate venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
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
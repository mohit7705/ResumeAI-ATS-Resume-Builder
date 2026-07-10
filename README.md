# 🚀 ResumeAI – AI-Powered ATS Resume Builder

ResumeAI is an AI-powered ATS Resume Builder that intelligently analyzes job descriptions and generates recruiter-friendly, ATS-optimized resumes.

Instead of manually editing resumes for every job, ResumeAI uses Google Gemini AI to:

- Analyze Job Descriptions
- Match Skills
- Rank Resume Projects
- Rewrite Project Highlights
- Generate an ATS Professional Summary
- Calculate ATS Score
- Generate ATS-Friendly HTML & PDF Resume

The project is built using FastAPI, React, TypeScript, Python, and Google Gemini.

# ✨ Features

- 🤖 AI Job Description Analysis
- 🧠 Semantic Skill Matching
- 📊 ATS Score Calculation
- 📈 AI Project Ranking
- ✍ AI Project Highlight Rewriting
- 📝 AI Professional Summary Generation
- 📄 ATS-Friendly Resume Generation
- 📑 HTML Resume Preview
- 📥 PDF Resume Export
- 🎯 Resume Optimization for Every Job Description

  
Step 3

— Tech Stack
# 🛠 Tech Stack

## Frontend

- React
- TypeScript
- Vite

## Backend

- Python
- FastAPI
- Pydantic

## AI

- Google Gemini API

## PDF

- Playwright

## Template Engine

- Jinja2

## Styling

- HTML
- CSS

Step 4 — Folder Structure

ResumeAI/
│
├── backend/
├── frontend/
├── templates/
├── generated/
│
├── data.example/
│   ├── personal/
│   │   ├── profile.json
│   │   ├── contact.json
│   │   ├── summary.json
│   │   ├── skills.json
│   │   ├── education.json
│   │   ├── experience.json
│   │   ├── certifications.json
│   │   └── achievements.json
│   │
│   └── projects/
│       └── projects.json
│
├── requirements.txt
├── .env.example
├── .gitignore


Step 5 

# 📥 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ResumeAI.git
```

Go inside the project

```bash
cd ResumeAI
```
Step 6

— Create Virtual Environment

Linux

python -m venv .venv

source .venv/bin/activate

Windows

python -m venv .venv

.venv\Scripts\activate

Step 7 
— Install Requirements

pip install -r requirements.txt

Step 8  — Install Playwright

playwright install chromium


Step 9 — Create .env

Create a file named

.env

Paste

```env
GOOGLE_API_KEY=YOUR_API_KEY

GOOGLE_MODEL=gemini-2.5-flash


```
Step 10  — Create Data Folder

Since personal information is not included in the repository, users need to create their own data directory.

data/
│
├── personal/
│
└── projects/

Step 11 — Create JSON Files

Inside

data/personal

Create

profile.json

contact.json

summary.json

skills.json

education.json

experience.json

certifications.json

achievements.json

Inside

data/projects

Create

projects.json


Step 12 — JSON Structure

Here you'll provide sample JSON for each file (e.g., profile.json, contact.json, projects.json, etc.) so users know the required format.

Step 13 — Run Backend

uvicorn backend.main:app --reload

Open

http://127.0.0.1:8000/docs


Step 14  — Run Frontend

cd frontend

npm install

npm run dev

Step 15 — How ResumeAI Works

Job Description

↓

Gemini AI Analysis

↓

Skill Matching

↓

Project Ranking

↓

Summary Generation

↓

Project Rewrite

↓

ATS Score

↓

Resume Builder

↓

HTML

↓

PDF

# 📜 License

This project is licensed under the MIT License.

Feel free to use, modify, and contribute.

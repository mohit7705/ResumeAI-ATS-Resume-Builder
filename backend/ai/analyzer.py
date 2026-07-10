import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


# --------------------------------------------------
# Google Gemini Configuration
# --------------------------------------------------

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("GOOGLE_MODEL")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

if not MODEL:
    raise ValueError("GOOGLE_MODEL not found in .env")


# --------------------------------------------------
# Initialize Gemini Client
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# Reusable AI Function
# --------------------------------------------------

def analyze(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the generated text.

    This function will be reused by all future AI modules.
    """

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        return str(response.text).strip()

    except Exception as e:
        raise RuntimeError(f"Gemini API Error: {str(e)}")


# --------------------------------------------------
# Job Description Analysis Prompt
# --------------------------------------------------


JOB_DESCRIPTION_PROMPT = """
You are an expert Technical Recruiter, Senior Hiring Manager, ATS Specialist, and AI Career Coach.

The input is a COMPLETE job posting copied from a company's careers page.

The posting may include:
- Company introduction
- Marketing content
- Benefits
- Equal opportunity statements
- Privacy policy
- Legal information
- Contact information

Ignore all unrelated content.

Focus ONLY on the actual job requirements.

Your task is to extract structured information that will later be used to:

1. Match resume skills
2. Rank resume projects
3. Rewrite resume projects
4. Generate an ATS-optimized summary
5. Calculate ATS score

Extract ONLY information that affects hiring decisions.

----------------------------------------
ROLE
----------------------------------------

Extract the exact role title.

----------------------------------------
EXPERIENCE
----------------------------------------

Extract the required experience.

Examples:

0-1 Years

1-3 Years

Fresher

2+ Years

----------------------------------------
TECHNICAL SKILLS
----------------------------------------

Extract ONLY explicit technical skills.

Examples:

Python
Java
JavaScript
TypeScript
React
Node.js
FastAPI
Spring Boot
Docker
Kubernetes
SQL
MongoDB
GraphQL
AWS
Azure
Git

----------------------------------------
ADVANCED AI SKILLS
----------------------------------------

Also detect modern AI concepts.

Examples:

LLM
Prompt Engineering
Agentic AI
AI Agents
Tool Calling
Function Calling
MCP
LangChain
LangGraph
CrewAI
RAG
Vector Database
Embeddings
Reasoning Models
Claude
Gemini
OpenAI
Cursor
Copilot

If these appear in the job posting,
include them in both:

skills

keywords

----------------------------------------
KEYWORDS
----------------------------------------

Extract ATS keywords.

These include:

Backend Development

Software Engineering

REST API

Microservices

Cloud Computing

Distributed Systems

Production Systems

System Design

Automation

Scalable Systems

Machine Learning

Computer Vision

Speech AI

Real-Time Systems

Customer Facing

Architecture

DevOps

CI/CD

----------------------------------------
RESPONSIBILITIES
----------------------------------------

Return concise responsibilities.

One sentence each.

Maximum 8.

----------------------------------------
RULES
----------------------------------------

Do NOT infer experience the job never mentions.

Do NOT invent skills.

Remove duplicates.

Normalize skill names.

Return ONLY valid JSON.

No markdown.

No explanation.

----------------------------------------
JSON
----------------------------------------

{{
    "role":"",
    "experience":"",
    "skills":[],
    "keywords":[],
    "responsibilities":[]
}}

Job Posting

{job_description}
"""


# --------------------------------------------------
# Job Description Analyzer
# --------------------------------------------------

def analyze_job_description(job_description: str) -> dict:
    """
    Analyze a Job Description and return structured JSON.
    """

    prompt = JOB_DESCRIPTION_PROMPT.format(
        job_description=job_description
    )

    response = analyze(prompt)

    # Debug raw Gemini response
    print("\n========== GEMINI RESPONSE ==========")
    print(response)
    print("=====================================\n")

    # Remove markdown formatting if Gemini adds it
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    # Extract JSON object only
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "Gemini did not return a valid JSON object."
        )

    json_text = response[start:end + 1]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by Gemini: {str(e)}"
        )
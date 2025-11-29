import uvicorn
import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime

# --- 1. FastAPI Application Setup ---
app = FastAPI(title="Creative Multi-Page Portfolio API")

# Get the project root directory (parent of api directory)
BASE_DIR = Path(__file__).resolve().parent.parent

# ADDED: Mount a static directory to serve assets like images and CSS.
# Path is relative to project root, not api directory
static_dir = str(BASE_DIR / "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initializes the Jinja2 template engine, looking for files in the 'templates' folder
# Path is relative to project root, not api directory
templates_dir = str(BASE_DIR / "templates")
templates = Jinja2Templates(directory=templates_dir)


# --- 2. Portfolio Data (Used by all pages) ---
PORTFOLIO_DATA = {
    "name": "Jeet Majumder",
    "title": "Junior Data Scientist & AI Enthusiast",
    "email": "jeet0912majumder@gmail.com",
    "linkedin": "jeet0912majumder",
    "github": "Jeet-047",
    "kaggle": "jeet047",
    "youtube": "@Jeet_047",
    "resume_path": "/static/jeet_majumder_resume.pdf", 
    "current_year": datetime.now().year, # Used in the footer
    
    # Page Route Mapping (Used in buttons)
    "pages": {
        "home": "/",
        "projects": "/projects",
        "resume": "/resume",
        "contact": "/contact",
    },

    # NEW: Navigation Links for the Header (Base Template)
    # This is required for the {% for page in data.nav_links %} loop in base.html
    "nav_links": [
        {"name": "Home", "url": "/"},
        {"name": "Projects", "url": "/projects"},
        {"name": "Resume", "url": "/resume"},
        {"name": "Contact", "url": "/contact"},
    ],
    
    # NEW: Data for Navbar Logo Animation (Base Template)
    # This is required for the typing animation in the logo
    "logo_suffixes": [".ai", ".ml", ".ds", ".ops"],

    # Data for Home Page Hero Animation
    "typing_sentences": [
        "scalable systems.",
        "beautiful frontends.",
        "robust APIs.",
        "innovative solutions."
    ],
    
    "qualifications": [
        {
            "degree": "M.S. Computer Science",
            "institution": "University of Tech Excellence",
            "year": "2018 - 2020",
            "details": "Specialized in Distributed Systems and Machine Learning Algorithms."
        },
        {
            "degree": "B.E. Software Engineering",
            "institution": "State Technical College",
            "year": "2014 - 2018",
            "details": "Focused on Data Structures and Web Application Development."
        }
    ],
    "skills": [
        {"name": "Python / FastAPI", "level": 95},
        {"name": "Tailwind CSS / Frontend", "level": 90},
        {"name": "React / TypeScript", "level": 85},
        {"name": "Database (SQL/NoSQL)", "level": 80},
        {"name": "Cloud Deployment (GCP/AWS)", "level": 75},
    ],
    "projects": [
        {
            "id": "project-1",
            "title": "Quantum Task Manager",
            "tech": "React, TypeScript, FastAPI",
            "desc": "A high-performance task management application featuring real-time collaboration and AI-driven prioritization. Implemented WebSocket communication.",
            "color": "bg-indigo-600",
            "icon": "🚀",
            "url": ""
        },
        {
            "id": "project-2",
            "title": "Decentralized Voting System",
            "tech": "Solidity, Web3.js, Python",
            "desc": "Developed a secure, transparent voting platform on the Ethereum blockchain. Focused on cryptographic security and smart contract auditing.",
            "color": "bg-emerald-600",
            "icon": "🔗",
            "url": ""
        },
        {
            "id": "project-3",
            "title": "Real-time Data Visualization",
            "tech": "Vue.js, D3.js, Pandas",
            "desc": "Built an interactive dashboard for visualizing large streaming datasets. Optimized rendering pipeline for 60fps performance on complex charts.",
            "color": "bg-rose-600",
            "icon": "📊",
            "url": ""
        }
    ],
    # Resume Data Structure - Required for resume.html
    "resume": {
        "name": "Jeet Majumder",
        "title": "Junior Data Scientist & AI Enthusiast",
        "bio": "Passionate Junior Data Scientist with a focus on building and deploying scalable machine learning models. Adept in data preprocessing, statistical analysis, and developing innovative AI solutions using Python and cloud platforms.",
        "contact": {
            "phone": "+91 98765 43210",
            "email": "jeet.majumder.dev@example.com",
            "location": "Kolkata, India",
            "linkedin": "https://linkedin.com/in/jeetmajumder-ds",
            "github": "https://github.com/jeetmajumder-ai"
        },
        "tech_stack": [
            "Python (Pandas, NumPy, Scikit-learn)",
            "TensorFlow / PyTorch",
            "SQL / NoSQL",
            "BigQuery",
            "Docker",
            "GCP / Azure ML",
            "Data Visualization (Matplotlib, Seaborn)"
        ],
        "awards": [
            {
                "title": "Data Science Capstone Project Excellence",
                "issuer": "University of Tech Excellence",
                "year": "2020"
            },
            {
                "title": "Kaggle Competitor (Top 10%)",
                "issuer": "Kaggle",
                "year": "2023"
            }
        ],
        "experience": [
            {
                "title": "Data Science Intern",
                "company": "Aether Analytics",
                "years": "2023 – Present",
                "details": [
                    "Developed and tested predictive models (Random Forest, XGBoost) to forecast customer churn, improving retention by 8%.",
                    "Performed ETL processes on large datasets (500GB+) using Pandas and SQL for feature engineering.",
                    "Created and maintained automated weekly reports and visualizations using Python and Tableau for stakeholders."
                ]
            },
            {
                "title": "Research Assistant, AI Lab",
                "company": "State Technical College",
                "years": "2021 – 2022",
                "details": [
                    "Contributed to a deep learning project focused on image classification using CNNs and PyTorch.",
                    "Managed version control for research code using Git and GitHub.",
                    "Wrote technical documentation and research papers detailing model architectures and performance metrics."
                ]
            }
        ],
        "education": [
            {
                "degree": "M.Sc. in Data Science & Analytics",
                "institution": "University of Tech Excellence",
                "year": "2020 – 2022",
                "details": "Thesis on Time-Series Forecasting using LSTM networks."
            },
            {
                "degree": "B.Tech in Information Technology",
                "institution": "City Engineering College",
                "year": "2016 – 2020",
                "details": "Specialized in database management and software development methodologies."
            }
        ]
    }
}


# --- 3. Page Endpoints (Routes) ---

@app.get("/")
async def home_page(request: Request):
    # Renders the 'home.html' template
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "data": PORTFOLIO_DATA, "active_page": "/"}
    )

@app.get("/projects")
async def projects_page(request: Request):
    # Renders the 'projects.html' template
    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "data": PORTFOLIO_DATA, "active_page": "/projects"}
    )

@app.get("/resume")
async def resume_page(request: Request):
    # Renders the 'resume.html' template
    return templates.TemplateResponse(
        "resume.html",
        {"request": request, "data": PORTFOLIO_DATA, "active_page": "/resume"}
    )

@app.get("/contact")
async def contact_page(request: Request):
    # Renders the 'contact.html' template
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "data": PORTFOLIO_DATA, "active_page": "/contact"}
    )


# --- 4. Running the Application ---
if __name__ == "__main__":
    # To run locally, use one of these methods:
    # Method 1: Run directly with Python (from project root):
    #   python api/index.py
    # Method 2: Run with uvicorn (from project root):
    #   uvicorn api.index:app --reload
    # 
    # Note: DO NOT use 'uvicorn main:app' - the file is now api/index.py
    # Ensure you have a 'templates' folder with HTML files and a 'static' folder for assets.
    uvicorn.run(app, host="0.0.0.0", port=8000)
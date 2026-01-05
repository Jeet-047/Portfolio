import uvicorn
import os
import yaml
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from api.models import ContactForm
from api.services.db_service import db_service
from api.services.email_service import email_service

# --- 1. FastAPI Application Setup ---
app = FastAPI(title="Creative Multi-Page Portfolio API")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# --- 2. Load Portfolio Data from YAML Files ---
CONFIGS_DIR = BASE_DIR / "configs"

def load_yaml_file(filename: str) -> dict:
    """Load and parse a YAML file from the configs directory."""
    file_path = CONFIGS_DIR / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# Load data from YAML files
static_data = load_yaml_file("static.yaml")
projects_data = load_yaml_file("projects.yaml")
resume_data = load_yaml_file("resume.yaml")

# Combine all data into PORTFOLIO_DATA
PORTFOLIO_DATA = {
    **static_data,  # Includes: name, title, email, linkedin, github, kaggle, youtube, resume_path, pages, nav_links, logo_suffixes, typing_sentences, qualifications, skills
    "current_year": datetime.now().year,  # Add current year dynamically
    **projects_data,  # Includes: projects
    **resume_data,  # Includes: resume
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

# --- NEW DYNAMIC PROJECT ROUTE ---
@app.get("/projects/{project_id}")
async def project_detail_page(request: Request, project_id: str):
    # Search for the project in our data list by ID
    project = next((p for p in PORTFOLIO_DATA["projects"] if p["id"] == project_id), None)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return templates.TemplateResponse(
        "project_detail.html", 
        {
            "request": request, 
            "data": PORTFOLIO_DATA, 
            "project": project,
            "active_page": "/projects"
        }
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


# --- Contact Form API Endpoint ---
@app.post("/api/contact")
async def submit_contact_form(form: ContactForm):
    """
    Handle contact form submission.
    Stores message in Supabase and sends auto-reply email.
    """
    try:
        # Prepare data for database
        data = {
            "name": form.name,
            "email": form.email,
            "subject": form.subject,
            "message": form.message,
        }
        
        # Store in Supabase
        db_response = db_service.insert_contact_message(data)
        
        # Send auto-reply email
        email_sent = email_service.send_auto_reply(
            recipient_email=form.email,
            name=form.name,
            subject=form.subject,
            message=form.message
        )
        
        # Return success response
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Your message has been received. Thank you!",
                "email_sent": email_sent
            }
        )
        
    except ValueError as e:
        # Handle missing environment variables
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        # Handle other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


# --- 4. Running the Application ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
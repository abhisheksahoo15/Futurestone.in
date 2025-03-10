from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
# import shutil
# import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import logging
import pickle

# Load the Pretrained ATS Model

# Initialize FastAPI app
app = FastAPI()

# Setup logging for Azure debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setting up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ensure necessary directories exist
os.makedirs("temp", exist_ok=True)
os.makedirs("ml_model", exist_ok=True)

@app.get("/")
async def home(request: Request):
    """ Serve the Landing Page """
    try:
        return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Web Page"})
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# resume builder app
@app.get("/dashboard/")
async def home(request: Request):
    """ Serve the Landing Page """
    try:
        return templates.TemplateResponse("dashboard.html", {"request": request, "title": "FastAPI Web Page"})
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# resume builder app
@app.get("/pricing/")
async def home(request: Request):
    """ Serve the Landing Page """
    try:
        return templates.TemplateResponse("pricing.html", {"request": request, "title": "FastAPI Web Page"})
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    




# carrear app
@app.get("/carrear/")
async def home(request: Request):
    """ Serve the Landing Page """
    try:
        return templates.TemplateResponse("carrear.html", {"request": request, "title": "FastAPI Web Page"})
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
# ---------------------- JOB FINDING FEATURE ----------------------





@app.post("/fetch-jobs/")
async def fetch_jobs(role: str = Form(...), location: str = Form(...)):
    """ Fetch job listings from LinkedIn (or another job board) """
    try:
        if not role or not location:
            raise HTTPException(status_code=400, detail="Role and location are required")

        # LinkedIn job search URL
        url = f"https://www.linkedin.com/jobs/search/?keywords={role}&location={location}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
        }

        response = requests.get(url, headers=headers)
        time.sleep(2)  # Prevent rate limiting

        if response.status_code != 200:
            logger.error(f"Failed to fetch job listings, Status Code: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to fetch job listings")

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="base-card")

        jobs = []
        for job in job_cards[:10]:  # Fetching top 10 jobs
            title_tag = job.find("h3", class_="base-search-card__title")
            company_tag = job.find("h4", class_="base-search-card__subtitle")
            link_tag = job.find("a", class_="base-card__full-link")

            title = title_tag.text.strip() if title_tag else "N/A"
            company = company_tag.text.strip() if company_tag else "N/A"
            job_link = link_tag["href"] if link_tag else "N/A"

            jobs.append({"title": title, "company": company, "link": job_link})

        return {"status": "success", "jobs": jobs}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail="Error fetching jobs")

# ---------------------- ERROR HANDLING ENDPOINT ----------------------

@app.get("/health/")
async def health_check():
    """ Simple health check endpoint to verify if the server is running """
    return {"status": "running", "message": "FastAPI service is up and running"}

# ---------------------- AZURE DEBUGGING ROUTE ----------------------

@app.get("/debug/")
async def debug_info():
    """ Debugging route to check if required files and directories exist """
    debug_data = {
        "temp_dir_exists": os.path.exists("temp"),
        "ml_model_dir_exists": os.path.exists("ml_model"),
        "ats_model_exists": os.path.exists(model_path),
        "ats_model_loaded": ats_model is not None,
    }
    return {"status": "debug", "data": debug_data}

from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import logging
import io

# Setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Logging for Azure or debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create required directories
os.makedirs("temp", exist_ok=True)
os.makedirs("ml_model", exist_ok=True)

# ---------------------- Basic HTML Pages ----------------------

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Web Page"})

@app.get("/dashboard/")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/pricing/")
async def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

@app.get("/carrear/")
async def carrear(request: Request):
    return templates.TemplateResponse("carrear.html", {"request": request})

@app.get("/case-study/")
async def case_study(request: Request):
    return templates.TemplateResponse("case-study.html", {"request": request})

@app.get("/contact_us/")
async def contact_us(request: Request):
    return templates.TemplateResponse("contact_us.html", {"request": request})

@app.get("/analytics/")
async def analytics_upload_page(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

# ---------------------- Job Fetching Feature ----------------------

@app.post("/fetch-jobs/")
async def fetch_jobs(role: str = Form(...), location: str = Form(...)):
    try:
        if not role or not location:
            raise HTTPException(status_code=400, detail="Role and location are required")

        url = f"https://www.linkedin.com/jobs/search/?keywords={role}&location={location}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
        }

        response = requests.get(url, headers=headers)
        time.sleep(2)

        if response.status_code != 200:
            logger.error(f"Failed to fetch job listings: {response.status_code}")
            raise HTTPException(status_code=500, detail="LinkedIn job search failed")

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="base-card")

        jobs = []
        for job in job_cards[:10]:
            title = job.find("h3", class_="base-search-card__title")
            company = job.find("h4", class_="base-search-card__subtitle")
            link = job.find("a", class_="base-card__full-link")

            jobs.append({
                "title": title.text.strip() if title else "N/A",
                "company": company.text.strip() if company else "N/A",
                "link": link["href"] if link else "N/A"
            })

        return {"status": "success", "jobs": jobs}

    except Exception as e:
        logger.error(f"Job fetch error: {e}")
        raise HTTPException(status_code=500, detail="Error while fetching jobs")

# ---------------------- Upload & Analyze CSV/Excel ----------------------

@app.post("/upload-data/")
async def upload_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename.lower()
        print("Filename:", filename)
        
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise ValueError("Unsupported file format")
        
        info = {
            "columns": list(df.columns),
            "shape": df.shape,
            "null_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "basic_stats": df.describe(include='all').fillna("N/A").to_dict()
        }

        return JSONResponse(content={"status": "success", "insights": info})

    except Exception as e:
        print("❌ ERROR during file processing:", str(e))
        raise HTTPException(status_code=400, detail=f"Failed to process the file: {str(e)}")

# ---------------------- Health & Debug Routes ----------------------

@app.get("/health/")
async def health_check():
    return {"status": "running", "message": "FastAPI service is up and running"}

@app.get("/debug/")
async def debug_info():
    return {
        "status": "debug",
        "temp_dir_exists": os.path.exists("temp"),
        "ml_model_dir_exists": os.path.exists("ml_model"),
    }

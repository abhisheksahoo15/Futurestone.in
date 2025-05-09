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
    return templates.TemplateResponse("/case-study/case1.html", {"request": request})

@app.get("/contact_us/")
async def contact_us(request: Request):
    return templates.TemplateResponse("contact_us.html", {"request": request})

@app.get("/analytics/")
async def analytics_upload_page(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/employee/")
async def analytics_upload_page(request: Request):
    return templates.TemplateResponse("register-worker.html", {"request": request})

@app.get("/founders/")
async def analytics_upload_page(request: Request):
    return templates.TemplateResponse("founders.html", {"request": request})


@app.get("/server/")
async def analytics_upload_page(request: Request):
    return templates.TemplateResponse("pagenotfound.html", {"request": request})


@app.get("/service/")
async def analytics_upload_page(request: Request):
    return templates.TemplateResponse("service.html", {"request": request})



# ---------------------- Job Fetching Feature ----------------------



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

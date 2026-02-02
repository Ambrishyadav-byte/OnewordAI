"""
FastAPI backend for OneWord AI Subtitle Generator.
Handles file uploads, transcription processing, and SRT downloads.
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import shutil
import asyncio
from typing import Optional, Dict
from datetime import datetime

from src.core.engine import SubtitleGenerator

app = FastAPI(title="OneWord AI Subtitle Generator")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Job storage (in-memory, replace with Redis for production)
jobs: Dict[str, dict] = {}


class JobStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


def process_video_task(
    job_id: str,
    input_path: str,
    model: str,
    language: Optional[str],
    mode: str
):
    """Background task to process video."""
    try:
        jobs[job_id]["status"] = JobStatus.PROCESSING
        jobs[job_id]["progress"] = 0
        
        # Create generator
        generator = SubtitleGenerator(model_name=model)
        
        # Process
        output_path = OUTPUT_DIR / f"{job_id}.srt"
        
        def progress_callback(percent):
            jobs[job_id]["progress"] = percent
        
        generator.process(
            input_path=input_path,
            output_path=str(output_path),
            language=language,
            mode=mode,
            progress_callback=progress_callback
        )
        
        jobs[job_id]["status"] = JobStatus.COMPLETED
        jobs[job_id]["progress"] = 100
        jobs[job_id]["output_file"] = str(output_path)
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        jobs[job_id]["status"] = JobStatus.FAILED
        jobs[job_id]["error"] = str(e)
        print(f"❌ Job {job_id} failed: {e}")



@app.get("/api/health")
async def health_check():
    """Health check."""
    return {"status": "ok", "service": "OneWord AI Subtitle Generator"}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a video/audio file.
    Returns a file_id for use in processing.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    # Save file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": file_path.stat().st_size
    }


@app.post("/api/process")
async def process_file(
    background_tasks: BackgroundTasks,
    file_id: str = Form(...),
    model: str = Form("base"),
    language: Optional[str] = Form(None),
    mode: str = Form("oneword")
):
    """
    Start processing a previously uploaded file.
    Returns a job_id to track progress.
    """
    # Find uploaded file
    uploaded_files = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    if not uploaded_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    input_path = str(uploaded_files[0])
    
    # Validate inputs
    if model not in ["tiny", "base", "small", "medium", "large"]:
        raise HTTPException(status_code=400, detail="Invalid model")
    
    if language and language not in ["hi", "en", "ur", "es"]:
        raise HTTPException(status_code=400, detail="Invalid language")
    
    if mode not in ["oneword", "twoword", "phrase"]:
        raise HTTPException(status_code=400, detail="Invalid mode")
    
    # Create job
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "job_id": job_id,
        "file_id": file_id,
        "status": JobStatus.PENDING,
        "progress": 0,
        "model": model,
        "language": language,
        "mode": mode,
        "created_at": datetime.now().isoformat()
    }
    
    # Start background task
    background_tasks.add_task(
        process_video_task,
        job_id, input_path, model, language, mode
    )
    
    return {"job_id": job_id}


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get processing status for a job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.get("/api/download/{job_id}")
async def download_srt(job_id: str):
    """Download the generated SRT file."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    output_file = Path(job["output_file"])
    if not output_file.exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        output_file,
        media_type="application/x-subrip",
        filename=f"subtitles_{job['mode']}.srt"
    )


# Mount static files (web UI) at root
app.mount("/", StaticFiles(directory="src/web", html=True), name="web")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

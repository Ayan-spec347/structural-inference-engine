# We added UploadFile and File here so FastAPI knows how to handle images
from fastapi import FastAPI, UploadFile, File, Request
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Importing your custom worker
from worker import run_defect_engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/ping")
def ping():
    return {"ping": "pong!"}

@app.post("/analyze/crack-detection")
async def analyze_image(file: UploadFile = File(...)):
    # 1. Save file temporarily inside the Linux Docker container
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb+") as f:
        f.write(file.file.read())
    
    # 2. Send the file path to the Redis queue
    task = run_defect_engine.delay(file_location)
    
    return {"task_id": task.id, "status": "Processing asynchronously"}

@app.get("/tasks/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
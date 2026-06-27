import os
import time
import subprocess
import json

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="process_structural_image")
def run_defect_engine(image_path: str):
    try:
        # We are calling our mock script here instead of engine.out for now
        result = subprocess.run(
            ['python', 'mock_engine.py', image_path],
            capture_output=True,
            text=True,
            check=True
        )
        bounding_boxes = json.loads(result.stdout)
        return {"status": "success", "detections": bounding_boxes}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

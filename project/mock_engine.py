# project/mock_engine.py
import sys
import time
import json

if __name__ == "__main__":
    # Simulate the heavy OpenCV/ONNX inference time
    time.sleep(3) 
    # Print fake bounding boxes for a surface crack to stdout
    print(json.dumps([{"label": "crack", "confidence": 0.92, "box": [120, 50, 300, 85]}]))
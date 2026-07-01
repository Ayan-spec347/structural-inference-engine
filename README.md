# Structural Inference Engine

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688)
![Redis](https://img.shields.io/badge/Redis-Message_Broker-dc382d)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ed)
![C++](https://img.shields.io/badge/C++-Inference_Engine-00599C)

A distributed, asynchronous backend architecture designed to ingest, queue, and process high-resolution structural imagery for defect detection without blocking the main web event loop.

##  Key Performance Metrics
* Architected an asynchronous **FastAPI/Redis** backend pipeline to process **100 concurrent structural streams** without main-thread blocking.
* Integrated a high-performance **C++ OpenCV/ONNX** inference worker to execute surface defect detection on **2,800+ image payloads**.
* Containerized a **4-node microservices architecture** with **Docker Compose** to guarantee zero-conflict, single-command production deployments.
* Conducted headless stress testing via **Locust**, validating an ultra-low **6ms median latency** and **35ms P99 response time**.

##  System Architecture

```mermaid
graph TD
    Client[Client Request / Image Upload] --> API[FastAPI Web Server]
    API -- Queues Task (Sub 50ms) --> Redis[(Redis Message Broker)]
    API -- Returns Task ID --> Client
    
    Redis <-- Polls for Tasks --> Celery[Celery Worker Node]
    
    subgraph Heavy Compute Node
        Celery -- Executes Subprocess --> CPP[C++ Defect Engine .out]
        CPP -- OpenCV / ONNX --> CPP
        CPP -- Returns JSON Detections --> Celery
    end
    
    Celery -- Updates Status --> Redis
    Client -- Polls /tasks/{id} --> API
    API -- Fetches Result --> Redis

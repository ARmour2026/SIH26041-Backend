from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import workers, modules, assessments, certificates, admin,auth

app = FastAPI(
    title="AR Industrial Safety Training & Certification API",
    version="1.0.0",
    description="Backend API supporting offline-first Android AR training for Jharkhand's mining, steel, and mica sectors."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workers.router)
app.include_router(modules.router)
app.include_router(assessments.router)
app.include_router(certificates.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "running", "message": "AR Safety Platform API is up and operational."}

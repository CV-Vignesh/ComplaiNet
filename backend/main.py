from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
import models
from routers import complaints

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Pharma Complaint AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(complaints.router)
from routers import ai
app.include_router(ai.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pharma Complaint AI API. API is running."}

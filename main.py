from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from GLH.router import GLH_router
from database import db

app = FastAPI()

app.middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins0)
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "GLH API is running!"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from GLH.router import GLH_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(GLH_router)

@app.get("/")
def root():
    return {"message": "GLH API is running!"}
from fastapi import FastAPI
from GLH.router import GLH_router

app = FastAPI()

app.include_router(GLH_router)

@app.get("/")
def root():
    return {"message": "GLH API is running!"}
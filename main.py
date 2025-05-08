# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.github import router as github_router
import httpx

app = FastAPI(title="Documentação Viva")

app.include_router(github_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Backend da Documentação Viva está no ar!"}
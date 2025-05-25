# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.github import router as github_router
from routes.stripe import router as stripe_router
import os
import uvicorn

app = FastAPI(title="Documentação Viva")

app.include_router(github_router)
app.include_router(stripe_router, prefix="/stripe")

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # usa a variável de ambiente ou 8000 como padrão
    uvicorn.run("main:app", host="0.0.0.0", port=port)
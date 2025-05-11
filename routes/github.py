import os
import zipfile
from fastapi import APIRouter, Request, Header, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import httpx
from dotenv import load_dotenv
import requests
from utils.file_utils import collect_code_files
from utils.send_docs_utils import send_to_n8n_webhook
from utils.ai_utils import analyze_file_with_ai

GITHUB_API = "https://api.github.com"
GITHUB_API_REPOS = "https://api.github.com/user/repos?per_page=100&sort=created"

load_dotenv()

router = APIRouter()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL")
FRONT_URL = os.getenv("FRONT_URL")

# Pasta onde vamos extrair os arquivos temporariamente
TEMP_DIR = "temp_repositories"
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/github/download-repo")
async def download_repo_zip(
    repo_owner: str,
    repo_name: str,
    token: str,
    user: str
):
    """
    Baixa o repositório em formato .zip e extrai para uma pasta temporária.
    """
    zip_url = f"{GITHUB_API}/repos/{repo_owner}/{repo_name}/zipball"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    try:
        # Baixa o conteúdo do zip
        response = requests.get(zip_url, headers=headers, stream=True)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Erro ao baixar repositório do GitHub",
            )

        zip_path = os.path.join(TEMP_DIR, f"{repo_owner}_{repo_name}.zip")

        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)

        # Extrai o zip
        extract_path = os.path.join(TEMP_DIR, f"{repo_owner}_{repo_name}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

        collected_files = collect_code_files(extract_path)
        total_amount_tokens_approximately = sum(
            item["amount_tokens_approximately"] for item in collected_files
        )

        print(f"Total de tokens aproximados: {total_amount_tokens_approximately}")

        for item in collected_files:
            print(f"Path: {item['path']}")
            ai_analysis = analyze_file_with_ai(item["path"], item["content"])
            print(f"AI analysis: {ai_analysis}")
            send_to_n8n_webhook(item["path"], ai_analysis, user)

        return JSONResponse(
            {
                "message": "Repositório baixado e extraído com sucesso",
                "path": extract_path,
                "total_amount_tokens_approximately": total_amount_tokens_approximately,
                "collected_files": collected_files,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")


@router.get("/github/repos")
async def list_repos(authorization: str = Header(...)):
    """
    Lista todos os repositórios do usuário autenticado no GitHub
    Requer o header: Authorization: Bearer <access_token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Token inválido")

    access_token = authorization.replace("Bearer ", "")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GITHUB_API_REPOS, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    repos = response.json()
    return [
        {
            "name": repo["name"],
            "full_name": repo["full_name"],
            "private": repo["private"],
            "html_url": repo["html_url"],
            "clone_url": repo["clone_url"],
        }
        for repo in repos
    ]


@router.get("/github/login")
async def login_github():
    redirect_uri = CALLBACK_URL
    github_oauth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&scope=repo"
    )
    return RedirectResponse(github_oauth_url)


@router.get("/github/callback")
async def github_callback(code: str):
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            token_url,
            headers=headers,
            data={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code},
        )
        token_data = response.json()
        access_token = token_data.get("access_token")

    if not access_token:
        return {"error": "Failed to obtain access token"}

    return RedirectResponse(f"{FRONT_URL}?token={access_token}")

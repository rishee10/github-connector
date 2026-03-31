import httpx
from fastapi import HTTPException
from app.core.config import settings


def get_github_headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


async def github_get(path: str, params: dict = None) -> dict | list:
    url = f"{settings.github_api_url}{path}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=get_github_headers(), params=params)
    _raise_for_status(response)
    return response.json()


async def github_post(path: str, payload: dict) -> dict:
    url = f"{settings.github_api_url}{path}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=get_github_headers(), json=payload)
    _raise_for_status(response)
    return response.json()


def _raise_for_status(response: httpx.Response):
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="GitHub token is invalid or expired.")
    if response.status_code == 403:
        raise HTTPException(status_code=403, detail="GitHub API rate limit exceeded or forbidden.")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Resource not found on GitHub.")
    if response.status_code == 422:
        raise HTTPException(status_code=422, detail=f"Validation error from GitHub: {response.json()}")
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"GitHub API error: {response.text}",
        )
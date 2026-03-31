from fastapi import APIRouter, Query
from app.services.github_client import github_get
from app.models.schemas import RepoResponse

router = APIRouter()


@router.get(
    "/{username}",
    response_model=list[RepoResponse],
    summary="List public repositories for a user or organization",
)
async def list_repos(
    username: str,
    per_page: int = Query(default=10, ge=1, le=100, description="Results per page (max 100)"),
    page: int = Query(default=1, ge=1, description="Page number"),
    sort: str = Query(default="updated", description="Sort by: created, updated, pushed, full_name"),
):
    """
    Fetch all public repositories for a GitHub user or organization.
    """
    data = await github_get(
        f"/users/{username}/repos",
        params={"per_page": per_page, "page": page, "sort": sort},
    )
    return [
        RepoResponse(
            id=r["id"],
            name=r["name"],
            full_name=r["full_name"],
            private=r["private"],
            html_url=r["html_url"],
            description=r.get("description"),
            language=r.get("language"),
            stargazers_count=r["stargazers_count"],
            forks_count=r["forks_count"],
            open_issues_count=r["open_issues_count"],
        )
        for r in data
    ]
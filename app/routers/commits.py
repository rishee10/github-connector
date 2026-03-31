from fastapi import APIRouter, Query
from app.services.github_client import github_get
from app.models.schemas import CommitResponse

router = APIRouter()


@router.get(
    "/{owner}/{repo}",
    response_model=list[CommitResponse],
    summary="Fetch commits from a repository",
)
async def list_commits(
    owner: str,
    repo: str,
    branch: str = Query(default="main", description="Branch name"),
    per_page: int = Query(default=10, ge=1, le=100),
    page: int = Query(default=1, ge=1),
):
    """
    Return a list of commits for the specified branch of a repository.
    """
    data = await github_get(
        f"/repos/{owner}/{repo}/commits",
        params={"sha": branch, "per_page": per_page, "page": page},
    )
    return [
        CommitResponse(
            sha=c["sha"],
            message=c["commit"]["message"],
            author=c["commit"]["author"]["name"],
            author_email=c["commit"]["author"]["email"],
            date=c["commit"]["author"]["date"],
            html_url=c["html_url"],
        )
        for c in data
    ]
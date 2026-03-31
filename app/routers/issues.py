from fastapi import APIRouter, Query
from app.services.github_client import github_get, github_post
from app.models.schemas import CreateIssueRequest, IssueResponse

router = APIRouter()


@router.get(
    "/{owner}/{repo}",
    response_model=list[IssueResponse],
    summary="List issues for a repository",
)
async def list_issues(
    owner: str,
    repo: str,
    state: str = Query(default="open", description="Filter by state: open, closed, all"),
    per_page: int = Query(default=10, ge=1, le=100),
    page: int = Query(default=1, ge=1),
):
    """
    List issues (excluding pull requests) for a given repository.
    """
    data = await github_get(
        f"/repos/{owner}/{repo}/issues",
        params={"state": state, "per_page": per_page, "page": page},
    )
    # GitHub issues endpoint also returns PRs — filter them out
    issues_only = [i for i in data if "pull_request" not in i]
    return [
        IssueResponse(
            id=i["id"],
            number=i["number"],
            title=i["title"],
            state=i["state"],
            html_url=i["html_url"],
            body=i.get("body"),
            user=i["user"]["login"],
            created_at=i["created_at"],
        )
        for i in issues_only
    ]


@router.post(
    "/{owner}/{repo}",
    response_model=IssueResponse,
    status_code=201,
    summary="Create a new issue in a repository",
)
async def create_issue(
    owner: str,
    repo: str,
    issue: CreateIssueRequest,
):
    """
    Create a new issue in the specified GitHub repository.
    Requires write access (your PAT must have `repo` scope).
    """
    payload = {"title": issue.title, "body": issue.body, "labels": issue.labels}
    data = await github_post(f"/repos/{owner}/{repo}/issues", payload)
    return IssueResponse(
        id=data["id"],
        number=data["number"],
        title=data["title"],
        state=data["state"],
        html_url=data["html_url"],
        body=data.get("body"),
        user=data["user"]["login"],
        created_at=data["created_at"],
    )
from pydantic import BaseModel, Field
from typing import Optional


# ── Repos ───────────────────────────────────────────────────────────────────

class RepoResponse(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: str
    description: Optional[str]
    language: Optional[str]
    stargazers_count: int
    forks_count: int
    open_issues_count: int


# ── Issues ──────────────────────────────────────────────────────────────────

class CreateIssueRequest(BaseModel):
    title: str = Field(..., min_length=1, description="Issue title")
    body: Optional[str] = Field(None, description="Issue body / description")
    labels: Optional[list[str]] = Field(default=[], description="List of label names")


class IssueResponse(BaseModel):
    id: int
    number: int
    title: str
    state: str
    html_url: str
    body: Optional[str]
    user: str
    created_at: str


# ── Commits ─────────────────────────────────────────────────────────────────

class CommitResponse(BaseModel):
    sha: str
    message: str
    author: str
    author_email: str
    date: str
    html_url: str
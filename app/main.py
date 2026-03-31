from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import repos, issues, commits

app = FastAPI(
    title="GitHub Cloud Connector",
    description="A FastAPI-based connector to GitHub's REST API. Supports repos, issues, and commits.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repos.router, prefix="/repos", tags=["Repositories"])
app.include_router(issues.router, prefix="/issues", tags=["Issues"])
app.include_router(commits.router, prefix="/commits", tags=["Commits"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "GitHub Cloud Connector is running 🚀"}
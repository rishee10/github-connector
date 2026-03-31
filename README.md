# GitHub Cloud Connector — FastAPI

A lightweight FastAPI backend that connects to the GitHub REST API.  
Supports listing repositories, managing issues, and fetching commits.

---

## 🚀 Features

| Endpoint | Method | Description |
|---|---|---|
| `GET /repos/{username}` | GET | List public repos for a user/org |
| `GET /issues/{owner}/{repo}` | GET | List issues for a repo |
| `POST /issues/{owner}/{repo}` | POST | Create a new issue |
| `GET /commits/{owner}/{repo}` | GET | Fetch commits from a repo |

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rishee10/github-connector.git
cd github-connector
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and paste your GitHub Personal Access Token:

```
GITHUB_TOKEN=ghp_your_token_here
```

> **How to create a PAT:**  
> GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)  
> Grant scopes: `repo` (full control) — needed to create issues.

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

---

## 📖 Interactive Docs

FastAPI auto-generates beautiful docs:

| URL | Description |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI (try endpoints live) |
| `http://127.0.0.1:8000/redoc` | ReDoc (clean reference) |

---

## 🔌 API Endpoints

### List Repositories

```
GET /repos/{username}?per_page=10&page=1&sort=updated
```

**Example:**
```bash
curl http://localhost:8000/repos/torvalds
```

---

### List Issues

```
GET /issues/{owner}/{repo}?state=open&per_page=10
```

**Example:**
```bash
curl http://localhost:8000/issues/microsoft/vscode
```

---

### Create an Issue

```
POST /issues/{owner}/{repo}
Content-Type: application/json
```

**Body:**
```json
{
  "title": "Bug: something is broken",
  "body": "Here is a detailed description of the issue.",
  "labels": ["bug"]
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/issues/YOUR_USERNAME/YOUR_REPO \
  -H "Content-Type: application/json" \
  -d '{"title": "Test issue", "body": "Created via API"}'
```

---

### Fetch Commits

```
GET /commits/{owner}/{repo}?branch=main&per_page=10
```

**Example:**
```bash
curl http://localhost:8000/commits/facebook/react?branch=main
```

---

## 📁 Project Structure

```
github-connector/
├── app/
│   ├── main.py              # FastAPI app + router registration
│   ├── core/
│   │   └── config.py        # Environment variable loading
│   ├── services/
│   │   └── github_client.py # Shared HTTP client for GitHub API
│   ├── routers/
│   │   ├── repos.py         # /repos endpoints
│   │   ├── issues.py        # /issues endpoints
│   │   └── commits.py       # /commits endpoints
│   └── models/
│       └── schemas.py       # Pydantic request/response models
├── .env.example             # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

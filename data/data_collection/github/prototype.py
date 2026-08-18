import requests
import json
from datetime import datetime, timezone
from pathlib import Path

URL = "https://api.github.com/search/repositories"

params = {
    "q": "RAG",
    "sort": "stars",
    "order": "desc",
    "per_page": 10
}

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "AI-Evolution-Intelligence-Prototype"
}

response = requests.get(
    URL,
    params=params,
    headers=headers,
    timeout=30
)

print("HTTP Status:", response.status_code)

response.raise_for_status()

data = response.json()

print("Repositories returned:", len(data.get("items", [])))

print(
    "Total matching repositories:",
    data.get("total_count")
)

print(
    "Rate limit remaining:",
    response.headers.get("X-RateLimit-Remaining")
)

for repo in data.get("items", []):

    created = repo.get("created_at")
    updated = repo.get("updated_at")

    print("\n---")
    print("Repository:", repo.get("full_name"))
    print("Description:", repo.get("description"))
    print("Stars:", repo.get("stargazers_count"))
    print("Forks:", repo.get("forks_count"))
    print("Open Issues:", repo.get("open_issues_count"))
    print("Language:", repo.get("language"))
    print("Topics:", repo.get("topics"))
    print("Created:", created)
    print("Updated:", updated)
    print("URL:", repo.get("html_url"))
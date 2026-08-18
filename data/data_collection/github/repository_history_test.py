import requests
import json
from datetime import datetime, timezone
from pathlib import Path

OWNER = "langgenius"
REPO = "dify"

URL = f"https://api.github.com/repos/{OWNER}/{REPO}/stargazers"

headers = {
    "Accept": "application/vnd.github.star+json",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "AI-Evolution-Intelligence-Prototype"
}

params = {
    "per_page": 10,
    "page": 1
}

response = requests.get(
    URL,
    params=params,
    headers=headers,
    timeout=30
)

print("HTTP Status:", response.status_code)

print(
    "Rate limit remaining:",
    response.headers.get("X-RateLimit-Remaining")
)

response.raise_for_status()

data = response.json()

print("Stargazers returned:", len(data))

for star in data:

    user = star.get("user", {})
    starred_at = star.get("starred_at")

    print("\n---")
    print("User:", user.get("login"))
    print("Starred At:", starred_at)

# Save raw response

output_dir = Path("data/raw/github")
output_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

output_file = output_dir / f"dify_stargazers_{timestamp}.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nRaw data saved to:", output_file)
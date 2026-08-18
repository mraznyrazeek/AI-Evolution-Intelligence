import requests
import json
from datetime import datetime, timezone

URL = "https://api.stackexchange.com/2.3/questions"

params = {
    "site": "stackoverflow",
    "tagged": "openai-api",
    "fromdate": 1704067200,
    "todate": 1706745600,
    "sort": "creation",
    "order": "asc",
    "pagesize": 100
}

response = requests.get(URL, params=params, timeout=30)

print("HTTP Status:", response.status_code)

response.raise_for_status()

data = response.json()

print("Items returned:", len(data.get("items", [])))
print("Quota remaining:", data.get("quota_remaining"))

for question in data.get("items", []):
    created = datetime.fromtimestamp(
        question["creation_date"],
        tz=timezone.utc
    )

    print("\n---")
    print("ID:", question["question_id"])
    print("Title:", question["title"])
    print("Tags:", question["tags"])
    print("Created:", created.isoformat())
    print("Score:", question.get("score"))
    print("Answers:", question.get("answer_count"))
    print("Views:", question.get("view_count"))


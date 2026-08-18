from huggingface_hub import HfApi
from datetime import datetime, timezone
import json
from pathlib import Path


api = HfApi()

models = api.list_models(
    search="llm",
    sort="created_at",
    limit=20
)

results = []

for model in models:

    record = {
        "model_id": model.id,
        "author": getattr(model, "author", None),
        "created_at": getattr(model, "created_at", None),
        "last_modified": getattr(model, "last_modified", None),
        "downloads": getattr(model, "downloads", None),
        "likes": getattr(model, "likes", None),
        "pipeline_tag": getattr(model, "pipeline_tag", None),
        "tags": getattr(model, "tags", None),
    }

    results.append(record)

    print("\n---")
    print("Model:", record["model_id"])
    print("Author:", record["author"])
    print("Created:", record["created_at"])
    print("Last Modified:", record["last_modified"])
    print("Downloads:", record["downloads"])
    print("Likes:", record["likes"])
    print("Pipeline:", record["pipeline_tag"])
    print("Tags:", record["tags"])


# Save raw prototype data

output_dir = Path("data/raw/huggingface")
output_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

output_file = output_dir / f"llm_models_{timestamp}.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        results,
        f,
        indent=2,
        ensure_ascii=False,
        default=str
    )

print("\nRaw data saved to:", output_file)
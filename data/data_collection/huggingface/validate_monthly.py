import json
from pathlib import Path
from datetime import datetime


DATA_DIR = Path("data/raw/huggingface/monthly")


def validate_file(file_path):
    result = {
        "file": file_path.name,
        "valid_json": False,
        "records": 0,
        "duplicate_model_ids": 0,
        "missing_model_ids": 0,
        "invalid_created_dates": 0,
        "status": "FAILED",
        "errors": [],
    }

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        result["valid_json"] = True

    except Exception as error:
        result["errors"].append(
            f"Invalid JSON: {error}"
        )
        return result

    if not isinstance(data, dict):
        result["errors"].append(
            "Root object is not a dictionary."
        )
        return result

    metadata = data.get("metadata")

    if not isinstance(metadata, dict):
        result["errors"].append(
            "Missing metadata."
        )

    records = data.get("records")

    if not isinstance(records, list):
        result["errors"].append(
            "Missing or invalid records list."
        )
        return result

    result["records"] = len(records)

    if len(records) == 0:
        result["errors"].append(
            "No records found."
        )

    model_ids = set()

    for record in records:

        if not isinstance(record, dict):
            result["errors"].append(
                "Non-dictionary record found."
            )
            continue

        model_id = record.get("model_id")

        if not model_id:
            result["missing_model_ids"] += 1
        else:
            if model_id in model_ids:
                result["duplicate_model_ids"] += 1

            model_ids.add(model_id)

        created_at = record.get("created_at")

        if created_at:

            try:
                datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                )

            except Exception:
                result["invalid_created_dates"] += 1

    if result["missing_model_ids"] > 0:
        result["errors"].append(
            f"Missing model_id: "
            f"{result['missing_model_ids']}"
        )

    if result["invalid_created_dates"] > 0:
        result["errors"].append(
            f"Invalid created_at values: "
            f"{result['invalid_created_dates']}"
        )

    if not result["errors"]:
        result["status"] = "PASS"
    else:
        result["status"] = "WARNING"

    return result


def main():

    print("=" * 70)
    print("AI Evolution Intelligence")
    print("Hugging Face Monthly Data Validator")
    print("=" * 70)

    files = sorted(
        DATA_DIR.glob("huggingface_*.json")
    )

    print()
    print(
        f"Files discovered: {len(files)}"
    )

    if not files:
        print(
            "ERROR: No monthly files found."
        )
        return

    results = []

    for file_path in files:

        print()
        print("-" * 70)
        print(
            f"Validating: {file_path.name}"
        )

        result = validate_file(
            file_path
        )

        results.append(result)

        print(
            f"Status: {result['status']}"
        )

        print(
            f"Records: {result['records']:,}"
        )

        print(
            f"Duplicate model IDs: "
            f"{result['duplicate_model_ids']:,}"
        )

        print(
            f"Missing model IDs: "
            f"{result['missing_model_ids']:,}"
        )

        print(
            f"Invalid created_at: "
            f"{result['invalid_created_dates']:,}"
        )

        if result["errors"]:

            for error in result["errors"]:
                print(
                    f"WARNING: {error}"
                )

    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    passed = sum(
        r["status"] == "PASS"
        for r in results
    )

    warnings = sum(
        r["status"] == "WARNING"
        for r in results
    )

    failed = sum(
        r["status"] == "FAILED"
        for r in results
    )

    total_records = sum(
        r["records"]
        for r in results
    )

    print(
        f"Files: {len(results)}"
    )

    print(
        f"Passed: {passed}"
    )

    print(
        f"Warnings: {warnings}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        f"Total records: "
        f"{total_records:,}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()
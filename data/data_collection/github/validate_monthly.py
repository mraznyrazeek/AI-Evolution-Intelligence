import json
from pathlib import Path
from datetime import datetime


DATA_DIR = Path("data/raw/github/monthly")


def parse_datetime(value):
    if not value:
        return False

    try:
        datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
        return True
    except Exception:
        return False


def validate_file(file_path):

    result = {
        "file": file_path.name,
        "valid_json": False,
        "records": 0,
        "duplicate_ids": 0,
        "missing_ids": 0,
        "missing_full_names": 0,
        "invalid_created_dates": 0,
        "invalid_updated_dates": 0,
        "invalid_period": 0,
        "status": "FAILED",
        "errors": [],
    }

    # --------------------------------------------------
    # Load JSON
    # --------------------------------------------------

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        result["valid_json"] = True

    except Exception as error:

        result["errors"].append(
            f"Invalid JSON: {error}"
        )

        return result

    # --------------------------------------------------
    # Root structure
    # --------------------------------------------------

    if not isinstance(data, dict):

        result["errors"].append(
            "Root object is not a dictionary."
        )

        return result

    required_root_keys = {
        "metadata",
        "technology_statistics",
        "records"
    }

    missing_root_keys = (
        required_root_keys -
        set(data.keys())
    )

    if missing_root_keys:

        result["errors"].append(
            "Missing root keys: "
            + ", ".join(sorted(missing_root_keys))
        )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata = data.get("metadata")

    if not isinstance(metadata, dict):

        result["errors"].append(
            "Metadata is missing or invalid."
        )

    else:

        required_metadata = {
            "source",
            "collection_type",
            "period_start",
            "period_end",
            "technologies"
        }

        missing_metadata = (
            required_metadata -
            set(metadata.keys())
        )

        if missing_metadata:

            result["errors"].append(
                "Missing metadata keys: "
                + ", ".join(
                    sorted(missing_metadata)
                )
            )

        if metadata.get("source") != "GitHub":

            result["errors"].append(
                "Metadata source is not GitHub."
            )

    # --------------------------------------------------
    # Records
    # --------------------------------------------------

    records = data.get("records")

    if not isinstance(records, list):

        result["errors"].append(
            "Records is missing or not a list."
        )

        return result

    result["records"] = len(records)

    if len(records) == 0:

        result["errors"].append(
            "No records found."
        )

    # --------------------------------------------------
    # Validate repository records
    # --------------------------------------------------

    repository_ids = set()

    for index, record in enumerate(records):

        if not isinstance(record, dict):

            result["errors"].append(
                f"Record {index} is not a dictionary."
            )

            continue

        # Required top-level fields

        if not record.get("technology"):

            result["errors"].append(
                f"Record {index}: missing technology."
            )

        if not record.get("search_query"):

            result["errors"].append(
                f"Record {index}: missing search_query."
            )

        repository = record.get("data")

        if not isinstance(repository, dict):

            result["errors"].append(
                f"Record {index}: missing data object."
            )

            continue

        # Repository ID

        repo_id = repository.get("id")

        if repo_id is None:

            result["missing_ids"] += 1

        else:

            if repo_id in repository_ids:

                result["duplicate_ids"] += 1

            repository_ids.add(repo_id)

        # Full name

        if not repository.get("full_name"):

            result["missing_full_names"] += 1

        # Created date

        created_at = repository.get(
            "created_at"
        )

        if not parse_datetime(created_at):

            result["invalid_created_dates"] += 1

        # Updated date

        updated_at = repository.get(
            "updated_at"
        )

        if updated_at and not parse_datetime(
            updated_at
        ):

            result["invalid_updated_dates"] += 1

    # --------------------------------------------------
    # Determine status
    # --------------------------------------------------

    if result["missing_ids"] > 0:

        result["errors"].append(
            f"Missing repository IDs: "
            f"{result['missing_ids']}"
        )

    if result["missing_full_names"] > 0:

        result["errors"].append(
            f"Missing full_name values: "
            f"{result['missing_full_names']}"
        )

    if result["invalid_created_dates"] > 0:

        result["errors"].append(
            f"Invalid created_at values: "
            f"{result['invalid_created_dates']}"
        )

    if result["invalid_updated_dates"] > 0:

        result["errors"].append(
            f"Invalid updated_at values: "
            f"{result['invalid_updated_dates']}"
        )

    if not result["errors"]:

        result["status"] = "PASS"

    else:

        result["status"] = "WARNING"

    return result


def main():

    print("=" * 70)
    print("AI Evolution Intelligence")
    print("GitHub Monthly Data Validator")
    print("=" * 70)

    files = sorted(
        DATA_DIR.glob("github_*.json")
    )

    print()
    print(
        f"Files discovered: {len(files)}"
    )

    if not files:

        print(
            "ERROR: No GitHub monthly files found."
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
            f"Records: "
            f"{result['records']:,}"
        )

        print(
            f"Duplicate repository IDs: "
            f"{result['duplicate_ids']:,}"
        )

        print(
            f"Missing IDs: "
            f"{result['missing_ids']:,}"
        )

        print(
            f"Missing full_name: "
            f"{result['missing_full_names']:,}"
        )

        print(
            f"Invalid created_at: "
            f"{result['invalid_created_dates']:,}"
        )

        print(
            f"Invalid updated_at: "
            f"{result['invalid_updated_dates']:,}"
        )

        for error in result["errors"]:

            print(
                f"WARNING: {error}"
            )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

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

    total_duplicates = sum(
        r["duplicate_ids"]
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

    print(
        f"Duplicate repository IDs: "
        f"{total_duplicates:,}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()
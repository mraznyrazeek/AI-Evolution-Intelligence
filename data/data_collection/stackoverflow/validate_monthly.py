import json
from pathlib import Path


DATA_DIR = Path("data/raw/stackoverflow/monthly")


def validate_file(file_path):

    result = {
        "file": file_path.name,
        "valid_json": False,
        "records": 0,
        "duplicate_question_ids": 0,
        "missing_question_ids": 0,
        "missing_titles": 0,
        "invalid_creation_dates": 0,
        "invalid_activity_dates": 0,
        "missing_tags": 0,
        "missing_search_queries": 0,
        "legacy_metadata": False,
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
        "records"
    }

    missing_root_keys = (
        required_root_keys -
        set(data.keys())
    )

    if missing_root_keys:

        result["errors"].append(
            "Missing root keys: "
            + ", ".join(
                sorted(missing_root_keys)
            )
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

        # Common required metadata
        common_metadata = {
            "source",
            "queries",
            "collection_timestamp",
            "raw_record_count",
            "unique_record_count"
        }

        missing_common = (
            common_metadata -
            set(metadata.keys())
        )

        if missing_common:

            result["errors"].append(
                "Missing metadata keys: "
                + ", ".join(
                    sorted(missing_common)
                )
            )

        # Source check
        if metadata.get("source") != "Stack Overflow":

            result["errors"].append(
                "Metadata source is not Stack Overflow."
            )

        # --------------------------------------------------
        # Modern metadata schema
        # --------------------------------------------------

        modern_keys = {
            "collection_type",
            "period_start",
            "period_end"
        }

        # --------------------------------------------------
        # Legacy metadata schema
        # --------------------------------------------------

        legacy_keys = {
            "study_period"
        }

        if modern_keys.issubset(metadata.keys()):

            # Modern schema is valid

            if metadata.get(
                "unique_record_count"
            ) != len(data.get("records", [])):

                result["errors"].append(
                    "Metadata unique_record_count "
                    "does not match actual records."
                )

        elif legacy_keys.issubset(metadata.keys()):

            # January 2023 legacy schema
            result["legacy_metadata"] = True

            if metadata.get(
                "unique_record_count"
            ) != len(data.get("records", [])):

                result["errors"].append(
                    "Legacy metadata "
                    "unique_record_count does not "
                    "match actual records."
                )

        else:

            result["errors"].append(
                "Unrecognized Stack Overflow "
                "metadata schema."
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
    # Validate question records
    # --------------------------------------------------

    question_ids = set()

    for index, record in enumerate(records):

        if not isinstance(record, dict):

            result["errors"].append(
                f"Record {index} is not a dictionary."
            )

            continue

        # Search query

        if not record.get("search_query"):

            result["missing_search_queries"] += 1

        # Question data

        question = record.get("data")

        if not isinstance(question, dict):

            result["errors"].append(
                f"Record {index}: missing data object."
            )

            continue

        # Question ID

        question_id = question.get(
            "question_id"
        )

        if question_id is None:

            result["missing_question_ids"] += 1

        else:

            if question_id in question_ids:

                result["duplicate_question_ids"] += 1

            question_ids.add(question_id)

        # Title

        if not question.get("title"):

            result["missing_titles"] += 1

        # Tags

        tags = question.get("tags")

        if not isinstance(tags, list):

            result["missing_tags"] += 1

        # Creation date

        creation_date = question.get(
            "creation_date"
        )

        if not isinstance(
            creation_date,
            (int, float)
        ):

            result["invalid_creation_dates"] += 1

        # Last activity date

        activity_date = question.get(
            "last_activity_date"
        )

        if not isinstance(
            activity_date,
            (int, float)
        ):

            result["invalid_activity_dates"] += 1

    # --------------------------------------------------
    # Record validation errors
    # --------------------------------------------------

    if result["missing_question_ids"] > 0:

        result["errors"].append(
            f"Missing question IDs: "
            f"{result['missing_question_ids']}"
        )

    if result["missing_titles"] > 0:

        result["errors"].append(
            f"Missing titles: "
            f"{result['missing_titles']}"
        )

    if result["missing_tags"] > 0:

        result["errors"].append(
            f"Missing/invalid tags: "
            f"{result['missing_tags']}"
        )

    if result["missing_search_queries"] > 0:

        result["errors"].append(
            f"Missing search queries: "
            f"{result['missing_search_queries']}"
        )

    if result["invalid_creation_dates"] > 0:

        result["errors"].append(
            f"Invalid creation dates: "
            f"{result['invalid_creation_dates']}"
        )

    if result["invalid_activity_dates"] > 0:

        result["errors"].append(
            f"Invalid activity dates: "
            f"{result['invalid_activity_dates']}"
        )

    # --------------------------------------------------
    # Determine final status
    # --------------------------------------------------

    if not result["errors"]:

        result["status"] = "PASS"

    else:

        result["status"] = "FAILED"

    return result


def main():

    print("=" * 70)
    print("AI Evolution Intelligence")
    print("Stack Overflow Monthly Data Validator")
    print("=" * 70)

    files = sorted(
        DATA_DIR.glob(
            "stackoverflow_*.json"
        )
    )

    print()
    print(
        f"Files discovered: {len(files)}"
    )

    if not files:

        print(
            "ERROR: No Stack Overflow "
            "monthly files found."
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
            f"Duplicate question IDs: "
            f"{result['duplicate_question_ids']:,}"
        )

        print(
            f"Missing question IDs: "
            f"{result['missing_question_ids']:,}"
        )

        print(
            f"Missing titles: "
            f"{result['missing_titles']:,}"
        )

        print(
            f"Missing/invalid tags: "
            f"{result['missing_tags']:,}"
        )

        print(
            f"Missing search queries: "
            f"{result['missing_search_queries']:,}"
        )

        print(
            f"Invalid creation dates: "
            f"{result['invalid_creation_dates']:,}"
        )

        print(
            f"Invalid activity dates: "
            f"{result['invalid_activity_dates']:,}"
        )

        if result["legacy_metadata"]:

            print(
                "Metadata: LEGACY SCHEMA "
                "(preserved)"
            )

        for error in result["errors"]:

            print(
                f"ERROR: {error}"
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

    failed = sum(
        r["status"] == "FAILED"
        for r in results
    )

    total_records = sum(
        r["records"]
        for r in results
    )

    total_duplicates = sum(
        r["duplicate_question_ids"]
        for r in results
    )

    legacy_files = sum(
        r["legacy_metadata"]
        for r in results
    )

    print(
        f"Files: {len(results)}"
    )

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        f"Legacy metadata files: "
        f"{legacy_files}"
    )

    print(
        f"Total records: "
        f"{total_records:,}"
    )

    print(
        f"Duplicate question IDs: "
        f"{total_duplicates:,}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()
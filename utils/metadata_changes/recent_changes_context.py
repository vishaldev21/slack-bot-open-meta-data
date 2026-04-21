import json
from .request import get_data


def get_changes(input: str) -> list | None:
    path = "/api/v1/tables/"
    table_data, error = get_data(f"{path}name/{input}")
    if error is not None:
        print(f"Error: {error}")
        return None
    if table_data is None:
        print("No data found")
        return None
    table_id = table_data["id"]
    version_data, err = get_data(f"{path}{table_id}/versions")
    if err is not None:
        print(f"Error: {err}")
        return None
    if version_data is None:
        print("No data found")
        return None

    versions = version_data.get("versions")
    if versions is not None and len(versions) >= 2:
        prev_version = json.loads(version_data["versions"][0])
        result = []
        if (
            "fieldsAdded" in prev_version["changeDescription"]
            and prev_version["changeDescription"]["fieldsAdded"] is not None
        ):
            added_result = "Fields added:\n"
            field_added = prev_version["changeDescription"]["fieldsAdded"]
            if len(field_added) == 0:
                added_result += "No fields added\n"
            for item in field_added:
                added_result += f"{item['newValue']}\n"

        if (
            "fieldsUpdated" in prev_version["changeDescription"]
            and prev_version["changeDescription"]["fieldsUpdated"] is not None
        ):
            updated_result = "Fields updated:\n"
            field_updated = prev_version["changeDescription"]["fieldsUpdated"]
            if len(field_updated) == 0:
                updated_result += "No fields updated\n"
            for item in field_updated:
                updated_result += f"{item['updatedValue']}\n"

        if (
            "fieldsDeleted" in prev_version["changeDescription"]
            and prev_version["changeDescription"]["fieldsDeleted"] is not None
        ):
            deleted_result = "Fields deleted:\n"
            field_deleted = prev_version["changeDescription"]["fieldsDeleted"]
            if len(field_deleted) == 0:
                deleted_result += "No fields deleted\n"
            for item in field_deleted:
                deleted_result += f"{item['oldValue']}\n"
        result = [added_result, updated_result, deleted_result]
        return result
    else:
        return None


def get_changes_wrapper(input: str) -> str:
    entity_changes = get_changes(input)
    if entity_changes is None:
        print("No changes found")
        return "No changes found"
    else:
        result = ""
        for change in entity_changes:
            result += change + "\n"
        return result

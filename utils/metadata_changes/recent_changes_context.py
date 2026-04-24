import json
from .request import get_data


def get_changes(entity, fqn: str) -> list | str:
    path = f"{entity}/name/{fqn}"
    entity_data, error = get_data(path)
    if error is not None:
        if error["status_code"] == 404 or error["status_code"] == 403:
            return "Please provide correct Fully Qualified Name"
    if entity_data is None:
        return "No changes done"
    entity_id = entity_data["id"]
    version_path = f"{entity}/{entity_id}/versions"
    version_data, err = get_data(version_path)
    if err is not None:
        return "Unexpected failure"
    if version_data is None:
        return "Unexpected failure"

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
                updated_result += (
                    f"Old value: {item['oldValue']}, New value: {item['newValue']}\n"
                )

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
        return "No changes has been done"


def get_changes_wrapper(entity, fqn: str) -> str:
    entity_changes = get_changes(entity, fqn)
    if type(entity_changes) is str:
        return entity_changes
    else:
        result = ""
        for change in entity_changes:
            result += change + "\n"
        return result

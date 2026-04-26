from ..state import State
import json
from constant import service_to_repo


def get_logs(state: State):
    reuslt_log = {}
    with open("logs/app.log") as f:
        for line in f:
            log = json.loads(line)
            if log["level"] == "ERROR":
                reuslt_log = log
    open("logs/app.log", "w").close()
    service = reuslt_log.get("service")
    if service is None:
        return {"logs": {}}
    owner_repo = service_to_repo[service]
    owner = owner_repo.split("/")[0]
    repo = owner_repo.split("/")[1]
    return {"logs": reuslt_log, "owner": owner, "repo": repo}

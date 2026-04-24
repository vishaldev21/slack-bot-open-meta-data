import httpx
import os
from dotenv import load_dotenv

load_dotenv()

host = "http://localhost:8585/api/v1/"
bot_access_token = os.environ.get("BOT_ACCESS_TOKEN")


def get_data(url: str):
    status_code = None
    try:
        r = httpx.get(
            f"{host}{url}",
            headers={"Authorization": f"Bearer {bot_access_token}"},
        )
        r.raise_for_status()
        status_code = r.status_code
        data = r.json()
        print(data)
        return data, None
    except Exception as e:
        return None, {"error": e, "status_code": status_code}

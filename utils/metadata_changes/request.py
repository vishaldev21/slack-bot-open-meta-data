import httpx
import os
from dotenv import load_dotenv

load_dotenv()

host = "http://localhost:8585"
bot_access_token = os.environ.get("BOT_ACCESS_TOKEN")


def get_data(url: str):
    try:
        r = httpx.get(
            f"{host}{url}",
            headers={"Authorization": f"Bearer {bot_access_token}"},
        )
        r.raise_for_status()
        data = r.json()
        return data, None
    except Exception as e:
        print(f"Error fetching tables: {e}")
        return None, e

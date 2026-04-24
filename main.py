from slack_bolt.adapter.socket_mode import SocketModeHandler
from app import app
import os

if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("APP_LEVEL_TOKEN")).start()
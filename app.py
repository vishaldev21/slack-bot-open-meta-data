import os
from slack_bolt import App
from utils import get_changes_wrapper
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ.get("BOT_OAUTH_TOKEN"))


@app.command("/hello")
def hello(ack, respond, command):
    ack()
    user_input = command.get("text")
    result = get_changes_wrapper(user_input)
    respond(result)

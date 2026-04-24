import os
from slack_bolt import App
from utils import get_changes_wrapper
from dotenv import load_dotenv
from utils import get_orphan_entity
from utils import get_impact_wrapper, get_impact #for impact analysis

load_dotenv()

app = App(token=os.environ.get("BOT_OAUTH_TOKEN"))


@app.command("/metadata_changes")
def hello(ack, respond, command):
    ack()
    [entity, fqn] = command.get("text").split(" ")
    entity = entity.strip()
    fqn = fqn.strip()
    result = get_changes_wrapper(entity, fqn)
    respond(result)


@app.command("/metadata_impact")
def impact(ack, respond, command):
    ack()
    [entity, fqn] = command.get("text").split(" ")
    entity = entity.strip()  
    fqn = fqn.strip()
    result = get_impact(entity,fqn)
    str_result = get_impact_wrapper(result)
    respond(str_result)



@app.command("/orphan-entity")
def orphan_entity(ack, respond, command):
    ack()
    user_input = command.get("text")
    entityType, fqn = user_input.split()
    entityType = entityType.strip()
    fqn = fqn.strip()
    data = get_orphan_entity(entityType, fqn)
    if type(data) is str:
        respond(data)
    elif type(data) is bool:
        if data:
            respond(f"{entityType} {fqn} is an orphan entity.")
        else:
            respond(f"{entityType} {fqn} is not an orphan entity.")
           

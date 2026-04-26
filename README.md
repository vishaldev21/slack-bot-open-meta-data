# Slack Bot for OpenMetadata

A beginner-friendly Slack bot that helps you work with metadata-related tasks from inside Slack.

This project currently supports these commands:

- `/metadata_changes <entity> <fqn>` — shows recent changes for a metadata entity
- `/metadata_impact <entity> <fqn>` — shows the impact analysis for an entity
- `/orphan-entity <entityType> <fqn>` — checks whether an entity is orphaned
- `/check-issue` — runs the agent workflow and returns the issue number, findings, and suggestions

## What this project does

This bot connects Slack with OpenMetadata-related logic so you can ask simple metadata questions without leaving Slack. The bot is built with Python, Slack Bolt, LangChain, and OpenMetadata ingestion packages.

## Requirements

Before you start, make sure you have:

- Python 3.12 or later
- A Slack app created in your Slack workspace
- Bot token and app-level token from Slack
- Access to the services or metadata source your bot is meant to query

## Project structure

```text
main.py        # Starts the Slack bot
app.py         # Slack commands and bot logic
services/      # Business logic for metadata checks and agent workflow
agent/         # Agent graph, state, and node logic
```

## Environment variables

Create a `.env` file in the project root and add the following values:

```env
BOT_OAUTH_TOKEN=xoxb-your-bot-token
APP_LEVEL_TOKEN=xapp-your-app-level-token
OPEN_AI_API_KEY=
GITHUB_ACCESS_TOKEN=
BOT_ACCESS_TOKEN
```

Depending on your setup, other services may also need their own credentials.

## Installation

1. Clone the repository

```bash
git clone https://github.com/vishaldev21/slack-bot-open-meta-data.git
cd slack-bot-open-meta-data
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies

If you are using `uv`:

```bash
uv sync
```

If you are using `pip`:

```bash
pip install -r requirements.txt
```

> Note: the repository uses `pyproject.toml`, so `uv sync` is the recommended option if you have `uv` installed.

## Slack setup

1. Create a Slack app in your workspace.
2. Add a bot user.
3. Enable Socket Mode.
4. Copy the bot token into `BOT_OAUTH_TOKEN`.
5. Copy the app-level token into `APP_LEVEL_TOKEN`.
6. Add the slash commands used by this project:
   - `/metadata_changes`
   - `/metadata_impact`
   - `/orphan-entity`
   - `/check-issue`
7. Install the app to your workspace.

## How to run

Start the bot with:

```bash
python main.py
```

The bot will connect to Slack using Socket Mode and wait for commands.

## How to use the commands

### 1) Metadata changes

```text
/metadata_changes <entity> <fqn>
```

Example:

```text
/metadata_changes table sample_db.public.users
```

### 2) Metadata impact

```text
/metadata_impact <entity> <fqn>
```

Example:

```text
/metadata_impact table sample_db.public.users
```

### 3) Orphan entity check

```text
/orphan-entity <entityType> <fqn>
```

Example:

```text
/orphan-entity table sample_db.public.users
```

### 4) Check issue

```text
/check-issue
```

This command runs the agent workflow and returns:

- the issue number
- the findings
- the fix suggestions

## Beginner notes

- `entity` and `entityType` are the type of metadata object you want to check, such as a table.
- `fqn` means fully qualified name. It is the exact name used to identify the object in your metadata system.
- The command text must usually contain the expected parts separated by spaces.

## Troubleshooting

### The bot does not start

Check that your `.env` file exists and both tokens are set correctly.

### Slack command returns an error

Make sure the slash command text is in the correct format. For example, some commands expect exactly two values: `entity` and `fqn`.

### `APP_LEVEL_TOKEN` or `BOT_OAUTH_TOKEN` is missing

Confirm that your environment variables are loaded before starting the bot.

### `uv` is not installed

Use `pip` with a virtual environment, or install `uv` first.

## Files you may want to look at

- `main.py` — starts the Slack Socket Mode handler
- `app.py` — defines the Slack slash commands
- `services/` — contains the actual metadata and agent logic
- `agent/` — contains the graph/state logic for the issue checker
  

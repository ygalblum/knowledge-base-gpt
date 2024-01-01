# Knowledge Base GPT

This repository includes the code to create a Knowledge Base GPT based on private information stored in a folder on Google Drive

## Acknowledgement

The application is based on [Langchain Python RAG PrivateGPT](https://github.com/jmorganca/ollama/tree/main/examples/langchain-python-rag-privategpt)

## Installation

### From source code

The source code distribution uses [Poetry](https://python-poetry.org/)

#### Install dependencies

```bash
poetry install
```

## Create the embedding database from a Google Drive

### Google Drive APIs

* Create a new project (or use an existing one) and enable Google Drive APIs
* Create a service account, generate a key `.json` file
* Store the file in the root directory under the name `service_key.json`

### Google Drive Folder ID

* Get the ID of the folder you would like to use for ingestion and set the environment variable
    ```bash
    export GOOGLE_DRIVE_FOLDER_ID=<Folder ID>
    ```

### Run the ingest script

```bash
./knowledge_base_gpt/apps/ingest/ingest.py
```

## Run the Slack Bot backend

### Slack Application

Use [manifest.yml](./slack/manifest.yml) to create a Slack Application

### Tokens

* Get the Bot and Application tokens and set the corresponding environment variables
    ```bash
    export SLACK_BOT_TOKEN=<Bot Token>
    export SLACK_APP_TOKEN=<Application Token>
    ```

### Run the Slack Bot backend

```bash
./knowledge_base_gpt/apps/slackbot/slack_bot.py
```
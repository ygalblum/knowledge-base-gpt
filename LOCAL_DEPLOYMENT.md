# Running the Slackbot locally

## Installation from source code

The source code distribution uses [Poetry](https://python-poetry.org/)

### Install dependencies

```bash
poetry install
```

## Create the embedding database from a Google Drive

### Create and store content

Create a Google Drive folder and safe all the documents in it. Please note, currently, shortcuts are not supported

### Grant access

Make sure the service account you created has access to the folder you would like to ingest


### Environment Variables

* Get the ID of the folder you would like to use for ingestion and set the environment variable
    ```bash
    export GOOGLE_DRIVE_FOLDER_ID=< Folder ID >
    ```
* Point the application to the service account file
    ```bash
    export SERVICE_KEY_FILE=< Path to the service key json file >
    ```

### Run the ingest script

```bash
./knowledge_base_gpt/apps/ingest/ingest.py
```

## Run a local Redis

The slackbot relies on [Redis](https://redis.io/) for storage.

You can use Podman and Quadlet to run it locally.

1. Create the file `~/.config/containers/systemd/redis.container`
    ```
    [Container]
    Image=docker.io/redis/redis-stack:latest
    PublishPort=6379:6379
    PublishPort=8001:8001
    ContainerName=redis
    ```
2. Reload the systemd daemon
    ```bash
    systemctl --user daemon-reload
    ```
3. Start the service
    ```bash
    systemctl --user start redis.service
    ```

## Run the proxy to the Ollama LLM
TBD

## Run the Slack Bot backend

### Environment Variables

* Get the Bot and Application tokens and set the corresponding environment variables
    ```bash
    export SLACK_BOT_TOKEN=<Bot Token>
    export SLACK_APP_TOKEN=<Application Token>
    ```
* Set the name of the slack channel to forward unanswered questions to
    ```bash
    export FORWARD_QUESTION_CHANNEL_NAME=<Channel Name>
    ```
* Set the location to store the chat logs
    ```bash
    export CHAT_LOGS_FILE=<Path to the chat log file>
    ```

### Run the Slack Bot backend

```bash
./knowledge_base_gpt/apps/slackbot/slack_bot.py
```
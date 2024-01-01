#!/usr/bin/env python3
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from knowledge_base_gpt.libs.gpt.private_gpt import PrivateGPT


app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
)


@app.message()
def got_message(message, say):
    answer = PrivateGPT.get_instance().answer_query(message['text'])
    say(answer)


def main():
    PrivateGPT.get_instance().initialize()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


if __name__ == "__main__":
    main()

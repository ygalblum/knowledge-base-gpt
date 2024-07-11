from pathlib import Path
import pytest
import requests


PROJECT_ROOT_PATH: Path = Path(__file__).parents[3]


@pytest.fixture
def slackbot_server_hostname():
    try:
        path = Path(PROJECT_ROOT_PATH) / "slack_server_url"
        with open(path, 'r') as file:
            ret = file.read()
    except FileNotFoundError:
        ret = "slack-server-mock:8080"
    return ret


def test_bot(slackbot_server_hostname):
    msg = "foo"
    # Send a message
    res = requests.post(url=f"http://{slackbot_server_hostname}/message", json={"message": msg})

    # Assert that the answer exists and that it is an echo of the message
    answer = res.json().get('answer')
    assert answer is not None
    assert answer == "0"

    # Assert that the one ephemeral message exists and that it is an echo of the message
    ephemeral_messages = res.json().get('ephemeral')
    assert ephemeral_messages is not None
    assert isinstance(ephemeral_messages, list)
    assert len(ephemeral_messages) == 1
    assert ephemeral_messages[0] == "On it. Be back with your answer soon"

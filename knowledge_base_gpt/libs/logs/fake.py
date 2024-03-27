""" Fake Chat fragment - used for testing """
from typing import Dict, Any

from knowledge_base_gpt.libs.logs.chat_fragment import ChatFragment


class FakeChatFragment(ChatFragment):  # pylint:disable=R0903
    """ Fake Chat log fragment """

    def _calculate_metrics(self, callback_handler: None) -> Dict[str, Any]:
        return {}

""" OpenAI Chat log fragment """
from typing import Dict, Any

from langchain_community.callbacks import OpenAICallbackHandler

from knowledge_base_gpt.libs.logs.chat_fragment import ChatFragment


class OpenAIChatFragment(ChatFragment):  # pylint:disable=R0903
    """ OpenAI Chat log fragment """

    def _calculate_metrics(self, callback_handler: OpenAICallbackHandler) -> Dict[str, Any]:
        return {
            "total_tokens": callback_handler.total_tokens,
            "prompt_tokens": callback_handler.prompt_tokens,
            "completion_tokens": callback_handler.completion_tokens,
            "successful_requests": callback_handler.successful_requests,
        }

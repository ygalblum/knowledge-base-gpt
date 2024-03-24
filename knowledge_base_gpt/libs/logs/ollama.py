""" Ollama Chat log fragment """
from knowledge_base_gpt.libs.logs.chat_fragment import ChatFragment
from knowledge_base_gpt.libs.gpt.ollama_info import OllamaCallbackHandler


class OllamaChatFragment(ChatFragment):  # pylint:disable=R0903
    """ Ollama Chat log fragment """

    def _calculate_metrics(self, callback_handler: OllamaCallbackHandler):
        metrics = callback_handler.metrics
        ret = {}
        answer_index = 0
        if len(metrics) > 1:
            ret['question_generation'] = metrics[0].to_json()
            answer_index = 1
        ret['answer_generation'] = metrics[answer_index].to_json()
        return ret

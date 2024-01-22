#!/bin/env python3
import logging

import gradio as gr
from langchain.schema import AIMessage, HumanMessage

from knowledge_base_gpt.libs.gpt.private_chat import PrivateChat

logger = logging.getLogger(__name__)

class KnowledgeBaseGradioException(Exception):
    pass


class KnowledgeBaseGradio():
    __instance = None

    @staticmethod
    def get_instance():
        if KnowledgeBaseGradio.__instance is None:
            KnowledgeBaseGradio()
        return KnowledgeBaseGradio.__instance

    def __init__(self):
        if KnowledgeBaseGradio.__instance is not None:
            raise KnowledgeBaseGradioException("This class is a singleton!")
        KnowledgeBaseGradio.__instance = self

    def run(self):
        self._private_chat = PrivateChat()
        chatbot=gr.Chatbot(
            label=f"LLM: Ollama",
            show_copy_button=True,
            elem_id="chatbot",
            render=False,
        )
        with gr.Blocks() as demo:
            with gr.Row(equal_height=False):
                with gr.Column(scale=7, elem_id="col"):
                    self._chat_interface = gr.ChatInterface(
                        self._handle_query,
                        chatbot=chatbot
                    )
            with gr.Row(equal_height=False):
                with gr.Column(scale=3):
                    ingest_button = gr.Button("Forward your question")
                    ingest_button.click(
                        self._forward_question,
                        inputs=chatbot
                    )
        demo.launch()

    @staticmethod
    def _messages_to_text(messages):
        text = ''
        for human, bot in messages:
            text += "Question: "
            text += human
            text += '\n'
            text += "Answer: "
            text += bot
            text += '\n'
        return text

    def _forward_question(self, chatbot):
        logger.error(self._messages_to_text(chatbot))

    def _handle_query(self, message, history):
        history_langchain_format = []
        for human, ai in history:
            history_langchain_format.append(HumanMessage(content=human))
            history_langchain_format.append(AIMessage(content=ai))
        answer = self._private_chat.answer_query(history_langchain_format, message)
        return answer['answer']


def main():
    try:
        KnowledgeBaseGradio.get_instance().run()
    except KnowledgeBaseGradioException as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import os
import time

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma


from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
)


model = os.environ.get("MODEL", "llama2-uncensored")
# For embeddings model, the example uses a sentence-transformers model
# https://www.sbert.net/docs/pretrained_models.html
# "The all-mpnet-base-v2 model provides the best quality, while all-MiniLM-L6-v2 is 5 times faster and still offers good quality."
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
persist_directory = os.environ.get("PERSIST_DIRECTORY", "db")
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))

from constants import CHROMA_SETTINGS

better_prompt_template = """
Use the following pieces of context to answer the question at the end. You can do two things:
 1. Return the answer to a question ONLY if the context contains the answer to the question.
 2. Return ONLY the text 'I dont know' if the context does not contain the answer to a question.

{context}

Question: {question}
Helpful Answer:
"""

PROMPT = PromptTemplate(
    template=better_prompt_template, input_variables=["context", "question"]
)

ollama_host = os.environ.get("OLLAMA_HOST", 'localhost')

class PrivateGPT():
    def __init__(self, hide_source):
        self._hide_source = hide_source

    def setup(self):
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
        llm = Ollama(model=model, base_url=f"http://{ollama_host}:11434")
        self._qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=not self._hide_source, chain_type_kwargs=dict(prompt=PROMPT, verbose=True))

    def handle_query(self, query, say):
        res = self._qa(query)
        answer, docs = res['result'], [] if self._hide_source else res['source_documents']
        say(answer)


def main():
    # Parse the command line arguments
    args = parse_arguments()
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]

    llm = Ollama(model=model, callbacks=callbacks, base_url=f"http://{ollama_host}:11434")

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents= not args.hide_source, chain_type_kwargs=dict(prompt=PROMPT, verbose=True))
    # Interactive questions and answers
    while True:
        query = input("\nEnter a query: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue

        # Get the answer from the chain
        start = time.time()
        res = qa(query)
        answer, docs = res['result'], [] if args.hide_source else res['source_documents']
        end = time.time()

        # Print the result
        print("\n\n> Question:")
        print(query)
        print(answer)

        # Print the relevant sources used for the answer
        for document in docs:
            print("\n> " + document.metadata["source"] + ":")
            print(document.page_content)

def parse_arguments():
    parser = argparse.ArgumentParser(description='privateGPT: Ask questions to your documents without an internet connection, '
                                                 'using the power of LLMs.')
    parser.add_argument("--hide-source", "-S", action='store_true',
                        help='Use this flag to disable printing of source documents used for answers.')

    parser.add_argument("--mute-stream", "-M",
                        action='store_true',
                        help='Use this flag to disable the streaming StdOut callback for LLMs.')

    return parser.parse_args()

private_gpt = PrivateGPT(True)

@app.message()
def got_message(message, say):
    private_gpt.handle_query(message['text'], say)
    # print(message)
    # say("back in a flash")

def new_main():
    private_gpt.setup()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

if __name__ == "__main__":
    new_main()

#!/usr/bin/env python3
import os

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


private_gpt = PrivateGPT(True)

@app.message()
def got_message(message, say):
    private_gpt.handle_query(message['text'], say)
    # print(message)
    # say("back in a flash")

def main():
    private_gpt.setup()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

if __name__ == "__main__":
    main()

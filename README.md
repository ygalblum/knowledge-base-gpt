# Knowledge Base GPT

This repository includes the code to create a Knowledge Base GPT based on private information stored in a folder on Google Drive

## Acknowledgement

The application is based on [Langchain Python RAG PrivateGPT](https://github.com/jmorganca/ollama/tree/main/examples/langchain-python-rag-privategpt)

## Prerequisites

### Slack Application

User the [manifest](./slack/manifest.yml) as a basis for your application

### Google Service Account

* Create a new project (or use an existing one) and enable Google Drive APIs
* Create a service account, generate a key `.json` file and store it locally

## Deploying the Ollama LLM

The ChatBot used [Ollama](https://ollama.com) as the LLM.

### VM for the LLM

To create a VM on Google Cloud Platform see the [README](./cloud/terraform/gcp/README.md)

### Deploy the LLM

Use the Ansible collection [Ollama](https://github.com/ygalblum/ansible-ollama-collection) to deploy Ollama on the created VM.

## Running the Slackbot on Kubernetes

See the Helm chart [README](./cloud/helm/README.md) for details on how to deploy the application on K8S

## Running the Slackbot locally

See [Local Deployment](./LOCAL_DEPLOYMENT.md) for the instructions

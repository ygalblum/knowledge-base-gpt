# Running the Slackbot on Kubernetes

## Prerequisites
The Helm chart assumes that [Certificate Manager](https://cert-manager.io/) is installed in the cluster

## Create the values file `myvals.yaml`
```yaml
ingestFolderID: < The ID of the Google Folder used to ingestion >
forwardChannel: < Name of the Channel to forward unanswered questions to >
slackAppToken: < Slack App token, starts with xapp >
slackBotToken: < Slack Bot token, starts with xoxb >
```

## Install the chart
```bash
helm install assistant  knowledgebase-slackbot/ -f myvals.yaml
```

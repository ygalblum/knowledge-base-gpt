# Running the Slackbot on Kubernetes

## Create the values file `myvals.yaml`
```yaml
vaultServerConfigMap: "vault-server-details"
vaultCredentialsSecret: "vault-server-credentials"
```

## Install the chart
```bash
helm install assistant  knowledgebase-slackbot/ -f myvals.yaml
```

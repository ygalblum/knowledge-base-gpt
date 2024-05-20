{{/*
Init container to fetch secrets from Vault
*/}}
{{- define "knowledgebase-slackbot.vault-init-container" -}}
- name: vault
  image: docker.io/hashicorp/vault:latest
  args:
  - "agent"
  - "-config=/vault/config/vault.hcl"
  volumeMounts:
  - name: vault-output
    mountPath: /vault-output
    readOnly: false
  - name: vault-credentials
    mountPath: /etc/vault-creds
    readOnly: true
  - name: vault-agent-config
    mountPath: /vault/config
    readOnly: true
  - name: vault-template
    mountPath: /vault/template
    readOnly: true
  - name: vault-ca-cert
    mountPath: /etc/vault-ca
    readOnly: true
  env:
  - name: SKIP_SETCAP
    value: "true"
  - name: VAULT_ADDR
    valueFrom:
      configMapKeyRef:
        name: {{ required "vaultServerConfigMap must be set" .Values.vaultServerConfigMap }}
        key: address
  - name: VAULT_CACERT
    value: "/etc/vault-ca/ca.crt"
{{- end }}


{{/*
List of volumes added to Pod spec for Vault
*/}}
{{- define "knowledgebase-slackbot.vault-volumes" -}}
- name: vault-output
  emptyDir:
    medium: Memory
    sizeLimit: 10Mi
- name: vault-ca-cert
  configMap:
    name: {{ required "vaultServerConfigMap must be set" .root.Values.vaultServerConfigMap }}
    items:
    - key: ca.crt
      path: ca.crt
- name: vault-credentials
  secret:
    secretName: {{ required "vaultCredentialsSecret must be set" .root.Values.vaultCredentialsSecret }}
- name: vault-agent-config
  configMap:
    name: {{ printf "%s" (include "knowledgebase-slackbot.vault-agent-config-configmap" .root) }}
- name: vault-template
  configMap:
    name: {{ .configMapName }}
{{- end }}

{{/*
Vault Agent configuration ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.vault-agent-config-configmap" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "vault-agent-config" }}
{{- end }}

{{/*
Vault Agent config
*/}}
{{- define "knowledgebase-slackbot.vault-agent-config" -}}
exit_after_auth = true
pid_file = "/tmp/pidfile"

auto_auth {
  method "approle" {
    mount_path = "auth/approle"
    config = {
      role_id_file_path = "/etc/vault-creds/role-id"
      secret_id_file_path = "/etc/vault-creds/secret-id"
      remove_secret_id_file_after_reading = false
    }
  }

  sink "file" {
    config = {
      path = "/tmp/vault-token-via-agent"
      mode = 0644
    }
  }
}

cache {
  use_auto_auth_token = true
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = true
}

template {
  source      = "/vault/template/vars.env.tmpl"
  destination = "/vault-output/vars.env"
}
{{- end }}

{{/*
Vault Template for Slackbot ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.vault-template-slackbot-configmap" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "vault-template-slackbot-configmap" }}
{{- end }}

{{/*
Vault Template for Slackbot
*/}}
{{- define "knowledgebase-slackbot.vault-template-slackbot" -}}
{{`
  {{- with secret "apps/cloud-marketplace-chatbot-admin/huggingface" }}
  export HUGGING_FACE_HUB_TOKEN='{{ .Data.data.token }}'
  {{ end }}
  {{- with secret "apps/cloud-marketplace-chatbot-admin/vllm" }}
  export OPENAI_API_KEY='{{ .Data.data.token }}'
  {{ end }}
  {{- with secret "apps/cloud-marketplace-chatbot-admin/slackbot" }}
  export SLACK_APP_TOKEN='{{ .Data.data.app_token }}'
  export SLACK_BOT_TOKEN='{{ .Data.data.bot_token }}'
  export FORWARD_QUESTION_CHANNEL_NAME='{{ .Data.data.forward_channel }}'
  {{ end }}
`}}
{{- end }}

{{/*
Vault Template for vLLM ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.vault-template-vllm-configmap" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "vault-template-vllm-configmap" }}
{{- end }}

{{/*
Vault Template for vLLM
*/}}
{{- define "knowledgebase-slackbot.vault-template-vllm" -}}
{{`
  {{- with secret "apps/cloud-marketplace-chatbot-admin/huggingface" }}
  export HUGGING_FACE_HUB_TOKEN='{{ .Data.data.token }}'
  {{ end }}
  {{- with secret "apps/cloud-marketplace-chatbot-admin/vllm" }}
  export VLLM_APP_TOKEN='{{ .Data.data.token }}'
  {{ end }}
`}}
{{- end }}

{{/*
Vault Template for Ingest ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.vault-template-ingest-configmap" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "vault-template-ingest-configmap" }}
{{- end }}

{{/*
Vault Template for Ingest
*/}}
{{- define "knowledgebase-slackbot.vault-template-ingest" -}}
{{`
  {{- with secret "apps/cloud-marketplace-chatbot-admin/google_drive" }}
  export GOOGLE_DRIVE_FOLDER_ID='{{ .Data.data.ingest_folder_id }}'
  export SERVICE_JSON='{{ .Data.data.service_json }}'
  {{ end }}
`}}
{{- end }}

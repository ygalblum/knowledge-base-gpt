{{/*
Knowledge Base configuration ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.knowledgebase-configmap" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "knowledgebase" }}
{{- end }}

{{/*
Knowledge Base Configuration
*/}}
{{- define "knowledgebase-slackbot.knowledgebase-config" -}}
slackbot:
  app_token: $SLACK_APP_TOKEN|""
  bot_token: $SLACK_BOT_TOKEN|""
  forward_channel: $FORWARD_QUESTION_CHANNEL_NAME|""

llm:
  mode: vllm

ollama:
  llm_model: {{ .Values.ollamaChatModel | quote }}
  embedding_model: {{ .Values.ollamaEmbeddingModel | quote }}

history:
  mode: redis

redis:
  host: "{{ include "knowledgebase-slackbot.redis-host" . }}"
  password: $REDIS_PASSWORD|""

log:
  chat_log_path: /logs/slackbot_chat_log.log

content_loader: {}

google_drive:
  service_key_file: $SERVICE_KEY_FILE|""
  folder_id: $GOOGLE_DRIVE_FOLDER_ID|""

text_splitter: {}

embedding:
  mode: hugging_face

hugging_face:
  embedding_model: $EMBEDDINGS_MODEL_NAME|all-MiniLM-L6-v2

vectorstore:
  persist_directory: "/db"

fake_model: {}

vllm:
  api_base: http://llm-service:8000/v1
  llm_model: $MODEL|instructlab/granite-7b-lab

{{- end }}

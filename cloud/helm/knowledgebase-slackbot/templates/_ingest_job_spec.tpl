{{/*
Ingest Job Spec. Reuse in initial job and crobjob
*/}}
{{- define "knowledgebase-slackbot.ingest-job-spec" -}}
spec:
  template:
    spec:
      containers:
      - name: ingest
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        command: ["python", "-m", "knowledge_base_gpt.apps.ingest"]
        volumeMounts:
        - name: embedding
          mountPath: "/db"
        - name: service-json
          mountPath: /usr/app/
        - mountPath: /etc/knowledgebase
          name: knowledgebase-config
        - mountPath: /.cache
          name: cache
        env:
        - name: KNOWLEDGE_BASE_SETTINGS_FOLDER
          value: /etc/knowledgebase
        - name: GOOGLE_DRIVE_FOLDER_ID
          valueFrom:
            secretKeyRef:
              name: {{ include "knowledgebase-slackbot.folder-id-secret" . }}
              key: folder-id
        - name: SERVICE_KEY_FILE
          value: /usr/app/service.json
        resources:
          limits:
            cpu: 1
            memory: 2Gi
      volumes:
      - name: knowledgebase-config
        configMap:
          name: {{ include "knowledgebase-slackbot.knowledgebase-configmap" . }}
      - name: embedding
        persistentVolumeClaim:
          claimName: {{ include "knowledgebase-slackbot.embedding-pvc" . }}
      - name: service-json
        secret:
          secretName: {{ include "knowledgebase-slackbot.service-json-secret" . }}
      - name: cache
        emptyDir:
          sizeLimit: 1Gi
      restartPolicy: Never
  backoffLimit: 4
{{- end }}
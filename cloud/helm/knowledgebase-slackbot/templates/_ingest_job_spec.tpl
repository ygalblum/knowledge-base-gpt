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
        command:
        - /bin/sh
        - -c
        - |
          until curl -fsI http://localhost:9901/ready; do echo \"Waiting for Sidecar...\"; sleep 3; done
          echo \"Sidecar available. Running the command...\";
          python -m "knowledge_base_gpt.apps.ingest";
          x=$(echo $?); curl -fsI -X POST http://localhost:9901/quitquitquit && exit $x
        volumeMounts:
        - name: embedding
          mountPath: "/db"
        - name: service-json
          mountPath: /usr/app/
        - mountPath: /etc/knowledgebase
          name: knowledgebase-config
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
        securityContext:
          runAsUser: 0
      - name: proxy
        image: "docker.io/envoyproxy/envoy:{{ .Values.envoyProxyImageTag }}"
        volumeMounts:
        - name: proxy-config
          mountPath: /etc/envoy
        - name: proxy-certificates
          mountPath: /etc/envoy-certificates
        env:
        - name: ENVOY_UID
          value: "0"
        resources:
          limits:
            cpu: 1
            memory: 1Gi
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
      - name: proxy-config
        configMap:
          name: {{ include "knowledgebase-slackbot.proxy-configmap" . }}
      - name: proxy-certificates
        secret:
          secretName: {{ include "knowledgebase-slackbot.proxy-certificate-secret" . }}
      restartPolicy: Never
  backoffLimit: 4
{{- end }}
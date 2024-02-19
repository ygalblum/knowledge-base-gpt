{{/*
FluentBit Parsers Configuration
*/}}
{{- define "knowledgebase-slackbot.fluentbit-parsers-conf" -}}
[PARSER]
    Name   knowledgebase_metrics
    Format json
    Time_Key time
    Time_Format %d/%b/%Y:%H:%M:%S %z
{{- end }}

{{/*
FluentBit Configuration
*/}}
{{- define "knowledgebase-slackbot.fluentbit-conf" -}}
[SERVICE]
    Parsers_File /fluent-bit-config/parsers.conf

[INPUT]
    Name tail
    Path /logs/slackbot_chat_log.log
    Tag chatlog
    Parser knowledgebase_metrics

[OUTPUT]
    name es
    match chatlog
    host {{ include "knowledgebase-slackbot.elasticsearch" .}}
    Index chat-log
    Suppress_Type_Name True

{{- end }}

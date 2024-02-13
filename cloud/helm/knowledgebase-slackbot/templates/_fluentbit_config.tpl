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
    Path /metrics/slackbot_metrics.log
    Tag metrics_file

[FILTER]
    Name parser
    Match metrics_file
    Key_Name log
    Parser knowledgebase_metrics

[FILTER]
    Name log_to_metrics
    Match metrics_file
    Tag eval_count_metric
    metric_mode histogram
    metric_name eval_count
    metric_description Number of token used to generate the answer
    value_field eval_count
    label_field identifier
    label_field stage
    bucket 50
    bucket 100
    bucket 300
    bucket 500
    bucket 1000
    bucket 2000
    bucket 5000

[OUTPUT]
    name prometheus_exporter
    match *metric
    host 0.0.0.0
    port 2021
{{- end }}
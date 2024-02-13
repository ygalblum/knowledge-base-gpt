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

{{- range $.Values.metricsFields }}
[FILTER]
    Name log_to_metrics
    Match metrics_file
    Tag {{ printf "%s_metric" .name }}
    metric_mode histogram
    metric_name {{ .name }}
    metric_description Number of token used to generate the answer
    value_field {{ .name }}
    label_field identifier
    label_field stage
{{- $buckets := get $.Values.metricsBuckets .type }}
{{- range $buckets }}
    bucket {{ . }}
{{- end }}

{{- end }}

[OUTPUT]
    name prometheus_exporter
    match *metric
    host 0.0.0.0
    port 2021
{{- end }}

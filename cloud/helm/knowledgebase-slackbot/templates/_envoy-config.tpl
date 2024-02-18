{{/*
Envoy Proxy configuration ConfigMap Name
*/}}
{{- define "knowledgebase-slackbot.proxy-configmap" -}}
{{- printf "%s-%s" (include "knowledgebase-slackbot.fullname" .) "proxy" }}
{{- end }}

{{/*
Envoy Forward Proxy mTLS Configuration
*/}}
{{- define "knowledgebase-slackbot.envoy-proxy-config" -}}
admin:
  address:
    socket_address:
      address: 0.0.0.0
      port_value: 9901
static_resources:
  listeners:
  - name: ollama_listener
    address:
      socket_address:
        address: 127.0.0.1
        port_value: 11434
    filter_chains:
    - filters:
      - name: envoy.filters.network.tcp_proxy
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
          stat_prefix: ollama_tcp
          cluster: ollama_cluster
  clusters:
  - name: ollama_cluster
    type: STRICT_DNS
    load_assignment:
      cluster_name: ollama_cluster
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: {{ .Values.ollamaServerAddress }}
                port_value: {{ .Values.ollamaServerSecurePort }}
    transport_socket:
      name: envoy.transport_sockets.tls
      typed_config:
        "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext
        common_tls_context:
          tls_certificates:
          - certificate_chain:
              filename: /etc/envoy-certificates/tls.crt
            private_key:
              filename: /etc/envoy-certificates/tls.key
          validation_context:
            match_typed_subject_alt_names:
            # - san_type: DNS
            #   matcher:
            #     exact: proxy-postgres-backend.example.com
            trusted_ca:
              filename: /etc/envoy-certificates/ca.crt
{{- end }}

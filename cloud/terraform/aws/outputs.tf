output "external_services_exteranl_dns" {
  description = "External DNS of the Ollama instalce"
  value = aws_instance.ollama.public_dns
}

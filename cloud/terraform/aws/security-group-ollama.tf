resource "aws_security_group" "ollama" {
  count = var.ollama_port == 0 ? 0 :1

  name = "Ollama"
  description = "Security group for Ollama LLM Port"
}

resource "aws_vpc_security_group_ingress_rule" "ollama" {
  count = var.ollama_port == 0 ? 0 :1

  security_group_id = aws_security_group.ollama[0].id

  ip_protocol = "tcp"
  from_port = var.ollama_port
  to_port = var.ollama_port
  cidr_ipv4 = local.myip_cidr
}

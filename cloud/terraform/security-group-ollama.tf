resource "aws_security_group" "ollama" {
  name = "Ollama"
  description = "Security group for Ollama for Ansible Automation Hub external services"
}

resource "aws_vpc_security_group_ingress_rule" "ollama" {
  security_group_id = aws_security_group.ollama.id

  ip_protocol = "tcp"
  from_port = var.ollama_port
  to_port = var.ollama_port
  cidr_ipv4 = local.myip_cidr
}

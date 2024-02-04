resource "aws_security_group" "webui" {
  count = var.expose_webui ? 1 : 0

  name = "Ollama - WebUI access"
  description = "Security group for Ollama WebUI"
}

resource "aws_vpc_security_group_ingress_rule" "http" {
  count = var.expose_webui ? 1 : 0

  security_group_id = aws_security_group.webui[0].id

  ip_protocol = "tcp"
  from_port = 80
  to_port = 80
  cidr_ipv4 = "0.0.0.0/0"
}

resource "aws_vpc_security_group_ingress_rule" "https" {
  count = var.expose_webui ? 1 : 0

  security_group_id = aws_security_group.webui[0].id

  ip_protocol = "tcp"
  from_port = 443
  to_port = 443
  cidr_ipv4 = "0.0.0.0/0"
}

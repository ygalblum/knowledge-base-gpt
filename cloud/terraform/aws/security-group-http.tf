resource "aws_security_group" "webui" {
  name = "Ollama - WebUI access"
  description = "Security group for Ollama WebUI"
}

resource "aws_vpc_security_group_ingress_rule" "http" {
  security_group_id = aws_security_group.webui.id

  ip_protocol = "tcp"
  from_port = 80
  to_port = 80
  cidr_ipv4 = "0.0.0.0/0"
}

resource "aws_vpc_security_group_ingress_rule" "https" {
  security_group_id = aws_security_group.webui.id

  ip_protocol = "tcp"
  from_port = 443
  to_port = 443
  cidr_ipv4 = "0.0.0.0/0"
}

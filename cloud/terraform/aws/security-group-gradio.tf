resource "aws_security_group" "gradio" {
  name = "Gradio"
  description = "Security group for Gradio UI"
}

resource "aws_vpc_security_group_ingress_rule" "gradio" {
  security_group_id = aws_security_group.gradio.id

  ip_protocol = "tcp"
  from_port = var.gradio_port
  to_port = var.gradio_port
  cidr_ipv4 = local.myip_cidr
}

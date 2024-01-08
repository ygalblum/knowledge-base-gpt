resource "aws_security_group" "outbound" {
  name = "Ygal - Allow all egress"
  description = "Allow all egress traffic"
}

resource "aws_vpc_security_group_egress_rule" "outbound_all" {
  security_group_id = aws_security_group.outbound.id
  ip_protocol = -1
  cidr_ipv4 = "0.0.0.0/0"
}

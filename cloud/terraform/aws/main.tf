data "http" "myip" {
  url = "http://ipv4.icanhazip.com"
}

data "aws_vpc" "current" {
  default = true
}

data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  myip_cidr = "${chomp(data.http.myip.response_body)}/32"
  vpc_cidr_block = "${data.aws_vpc.current.cidr_block}"
  security_group_ids = concat(
    concat(
      [aws_security_group.ssh.id, aws_security_group.outbound.id],
      var.expose_webui ? [aws_security_group.webui[0].id] : []
    ),
    var.ollama_port == 0 ? [] : [aws_security_group.ollama[0].id]
  )
}

data "aws_ami" "latest_centos_ami" {
  most_recent = true
  owners = ["125523088429"]
  filter {
    name   = "name"
    values = ["CentOS Stream 9 x86_64*"]
  }
}

resource "aws_instance" "ollama" {
    tags = {
        Name = "Ygal-Ollama"
    }

    ami           = data.aws_ami.latest_centos_ami.arn
    instance_type = var.ollama_instance_type

    key_name = var.key_name

    vpc_security_group_ids = tolist(local.security_group_ids)

    root_block_device {
      volume_size = var.ollama_volume_size
    }
}

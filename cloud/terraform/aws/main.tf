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
}

resource "aws_instance" "ollama" {
    tags = {
        Name = "Ygal-Ollama"
    }

    ami           = var.ollama_ami
    instance_type = var.ollama_instance_type

    key_name = var.key_name

    vpc_security_group_ids = [
      aws_security_group.ssh.id,
      aws_security_group.ollama.id,
      aws_security_group.gradio.id,
      aws_security_group.outbound.id,
    ]

    root_block_device {
      volume_size = var.ollama_volume_size
    }
}

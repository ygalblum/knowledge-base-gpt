module "ollama" {
    source = "git@github.com:ygalblum/terraform-module-aws-instance.git"

    ssh_key_name = var.ssh_key_name
    instance_name = var.instance_name
    instance_type = var.instance_type
    volume_size = var.volume_size
    application_ports = [8443, 19901, 12021]
}

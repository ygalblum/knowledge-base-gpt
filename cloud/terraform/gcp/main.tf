module "ollama" {
    source = "git@github.com:ygalblum/terraform-module-gcp-instance.git"

    gcp_project = "${var.gcp_project}"
    gcp_region = "${var.gcp_region}"
    ssh_public_key = "${var.ssh_public_key}"
    service_account = "${var.service_account}"
    name = "${var.name}"
    application_ports = [11435, 19901, 12021]
    additional_scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    accelerator_count = 1
}

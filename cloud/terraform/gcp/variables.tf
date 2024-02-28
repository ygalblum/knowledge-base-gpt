variable "gcp_project" {
    type = string
}

variable "gcp_region" {
    type = string
}

variable "ssh_public_key" {
  type = string
}

variable "service_account" {
    type = string
}

variable "name" {
    type = string
    default = "ollama"
}

variable "machine_type" {
    type = string
    default = "n1-standard-4"
}

variable "accelerator_types" {
    type = string
    default = "nvidia-tesla-t4"

}

variable "boot_image_size" {
    type = number
    default = 30
}

variable "ip_cidr_range" {
    type=string
    description="List of The range of internal addresses that are owned by this subnetwork."
    default="172.18.0.0/24"
}

variable "ssh_port" {
    type = number
    default = 22
}

variable "secured_ollama_port" {
    type = number
    default = 11435
}

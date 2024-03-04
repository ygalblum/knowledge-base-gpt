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

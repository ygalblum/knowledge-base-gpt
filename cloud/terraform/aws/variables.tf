variable "key_name" {
  type = string
}

variable "ollama_instance_type" {
    type = string
    default = "g4dn.xlarge"
}

variable "ollama_volume_size" {
    type = number
    default = 30

}

variable "ssh_port" {
    type = number
    default = 22
}

variable "ollama_port" {
    type = number
    default = 11434
}

variable "expose_webui" {
    type = bool
    default = false
}

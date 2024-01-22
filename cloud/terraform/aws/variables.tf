variable "key_name" {
  type = string
}

variable "ollama_ami" {
    type = string
    # Fedora 37
    # default = "ami-03150c0722010627e"
    # CentOS on us-east-1
    default = "ami-0efb76882af9859da"
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

variable "gradio_port" {
    type = number
    default = 7860
}

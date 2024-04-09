variable "ssh_key_name" {
  type = string
}

variable "instance_name" {
    type = string
    default = "llm"
}

variable "instance_type" {
    type = string
    default = "g5.xlarge"
}

variable "volume_size" {
    type = number
    default = 50
}

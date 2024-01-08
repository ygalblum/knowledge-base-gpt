output "external_ip" {
  description = "External IP for Instance"
  value = google_compute_instance.ollama.network_interface[0].access_config[0].nat_ip
}

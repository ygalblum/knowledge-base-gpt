terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
    http = {
      source = "hashicorp/http"
    }
  }
}

provider "google" {
  project     = var.gcp_project
  region      = var.gcp_region
}

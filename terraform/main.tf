provider "google" {
  project = "commanding-bee-443615-n7"
  region  = "us-central1"
}

resource "google_container_cluster" "primary" {
  name               = "primary-cluster"
  location           = "us-central1"
  initial_node_count = 1

  node_config {
    machine_type = "e2-small"
    disk_size_gb = 25
  }

  deletion_protection = false
}

output "kubernetes_cluster_name" {
  value = google_container_cluster.primary.name
}

output "kubernetes_cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
}

output "kubernetes_cluster_ca_certificate" {
  value = google_container_cluster.primary.master_auth.0.cluster_ca_certificate
}

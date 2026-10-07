output "namespace" {
  value       = kubernetes_namespace.homework.metadata[0].name
  description = "Kubernetes namespace created"
}

output "release_status" {
  value       = helm_release.homework.status
  description = "Status of the deployed Helm release"
}

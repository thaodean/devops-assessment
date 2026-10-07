variable "namespace" {
  type        = string
  default     = "production"
  description = "Kubernetes namespace for the application"
}

variable "environment" {
  type        = string
  default     = "prod"
  description = "Environment name passed to the deployment"
}

variable "image_tag" {
  type        = string
  default     = "1.0.0"
  description = "Tag of the container image to deploy"
}

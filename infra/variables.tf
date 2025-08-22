variable "region" {
  description = "AWS region"
  type = string
  default = "eu-north-1"
}

variable "cluster_name" {
 description = "EKS cluster name"
  type = string
  default = "audiovault-eks"
}

variable "cluster_version" {
  description = "EKS cluster version"
  type = string
  default = "1.32"
}

variable "namespace" {
  description = "cluster namespace for application"
  type = string
  default = "audiovault"
}
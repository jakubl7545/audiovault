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

variable "private_subnets" {
  description = "Private subnets addresses for VPC"
  type = list(string)
  default = ["10.0.0.0/20", "10.0.16.0/20"]
}

variable "public_subnets" {
  description = "Public subnets addresses for VPC"
  type = list(string)
  default = ["10.0.32.0/20", "10.0.48.0/20"]
}

variable "intra_subnets" {
  description = "Intra subnets addresses for VPC"
  type = list(string)
  default = ["10.0.64.0/24", "10.0.65.0/24"]
}

variable "database_subnets" {
  description = "Database subnets addresses for VPC"
  type = list(string)
  default = ["10.0.66.0/24", "10.0.67.0/24"]
}

variable "elasticache_subnets" {
  description = "Elasticache subnets addresses for VPC"
  type = list(string)
  default = ["10.0.68.0/24", "10.0.69.0/24"]
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.1.1"

  name = "audiovault-vpc"
  azs = ["eu-north-1a", "eu-north-1b"]
  cidr = "10.0.0.0/16"
  private_subnets = ["10.0.0.0/20", "10.0.16.0/20"]
  public_subnets = ["10.0.32.0/20", "10.0.48.0/20"]
  intra_subnets = ["10.0.64.0/24", "10.0.65.0/24"]
  database_subnets = ["10.0.66.0/24", "10.0.67.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
  private_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}

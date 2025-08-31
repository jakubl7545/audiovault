module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.1.1"

  name = "audiovault-vpc"
  azs = ["eu-north-1a", "eu-north-1b"]
  cidr = "10.0.0.0/16"
  private_subnets = var.private_subnets
  public_subnets = var.public_subnets
  intra_subnets = var.intra_subnets
  database_subnets = var.database_subnets
  elasticache_subnets = var.elasticache_subnets
  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb" = "1"
  }
  private_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

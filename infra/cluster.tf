module "eks" {
  source = "terraform-aws-modules/eks/aws"
  version = "~> 20.31"

  cluster_name = var.cluster_name
  cluster_version = var.cluster_version
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.intra_subnets
  cluster_endpoint_public_access = true
enable_cluster_creator_admin_permissions = true

  eks_managed_node_groups = {
    one = {
      name = "${var.cluster_name}-ng1"
      instance_types = ["t3.small"]
      min_size     = 2
      max_size     = 6
      desired_size = 2
    }
  }
}

resource "kubernetes_namespace" "audiovault" {
  metadata {
    name = var.namespace
  }
}

resource "null_resource" "update_kubeconfig" {
  depends_on = [module.eks]
  provisioner "local-exec" {
    command = "aws eks update-kubeconfig --name ${var.cluster_name}"
  }
}
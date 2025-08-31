locals {
  service_account_efs = "efs-csi-controller"
}

module "efs_role" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.55.0"
  role_name = "efs_csi_role"
  attach_efs_csi_policy = true
  oidc_providers = {
    eks = {
      provider_arn = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:${local.service_account_efs}"]
    }
  }
}

resource "helm_release" "aws_efs_csi_driver" {
  chart = "aws-efs-csi-driver"
  repository = "https://kubernetes-sigs.github.io/aws-efs-csi-driver/"
  name = "aws-efs-csi-driver"
  version = "3.1.9"
  namespace = "kube-system"
  set {
    name = "image.repository"
    value = "602401143452.dkr.ecr.${var.region}.amazonaws.com/eks/aws-efs-csi-driver"
  }
  set {
    name = "controller.serviceAccount.create"
    value = true
  }
  set {
    name = "controller.serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = module.efs_role.iam_role_arn
  }
  set {
    name = "controller.serviceAccount.name"
    value = local.service_account_efs
  }
}

resource "aws_security_group" "audiovault_efs_sg" {
  name = "audiovault_efs_sg"
  description = "Allow NFS access for EFS on port 2049"
  vpc_id = module.vpc.vpc_id
  ingress {
    from_port = 2049
    to_port = 2049
    protocol = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_efs_file_system" "audiovault_efs" {
  creation_token = "efs_for_audiovault"
}

resource "aws_efs_mount_target" "audiovault_efs_mount" {
  file_system_id = aws_efs_file_system.audiovault_efs.id
  security_groups = [aws_security_group.audiovault_efs_sg.id]
    for_each = var.private_subnets
    subnet_id = each.value
}
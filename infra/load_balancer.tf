locals {
  service_account_alb = "aws-load-balancer-controller"
}

module "lb_role" {
  source = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  version = "~> 5.55.0"
  role_name = "aws_load_balancer_controller_role"
  attach_load_balancer_controller_policy = true
  oidc_providers = {
    eks = {
      provider_arn = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:${local.service_account_alb}"]
    }
  }
}

resource "kubernetes_service_account" "alb_controller_sa" {
  metadata {
    name = local.service_account_alb
    namespace = "kube-system"
    labels = {
      "app.kubernetes.io/name" = local.service_account_alb
      "app.kubernetes.io/component" = "controller"
    }
    annotations = {
      "eks.amazonaws.com/role-arn" = module.lb_role.iam_role_arn
      "eks.amazonaws.com/sts-regional-endpoints" = "true"
    }
  }
}

resource "helm_release" "alb_controller" {
  name = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart = "aws-load-balancer-controller"
  version = "1.13.0"
  namespace = "kube-system"
  depends_on = [kubernetes_service_account.alb_controller_sa]
  set {
    name = "region"
    value = var.region
  }
  set {
    name = "vpcId"
    value = module.vpc.vpc_id
  }
  set {
    name = "image.repository"
    value = "602401143452.dkr.ecr.${var.region}.amazonaws.com/amazon/aws-load-balancer-controller"
  }
  set {
    name = "serviceAccount.create"
    value = "false"
  }
  set {
    name = "serviceAccount.name"
    value = local.service_account_alb
  }
  set {
    name = "clusterName"
    value = var.cluster_name
  }
}

module "eks-external-dns" {
  source  = "lablabs/eks-external-dns/aws"
  version = "1.2.0"
  cluster_identity_oidc_issuer =  module.eks.cluster_oidc_issuer_url
  cluster_identity_oidc_issuer_arn = module.eks.oidc_provider_arn
  settings = {
    "policy" = "sync"
  }
  depends_on = [module.eks]
}
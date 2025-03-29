locals {
  service_account = "secrets-csi-sa"
}

data "aws_secretsmanager_secret" "secrets_csi" {
  name = "audiovault"
}

data "aws_secretsmanager_secret_version" "current" {
  secret_id = data.aws_secretsmanager_secret.secrets_csi.id
}

resource "helm_release" "secrets_store_csi_driver" {
  name = "secrets-store-csi-driver"
  repository = "https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts"
  chart = "secrets-store-csi-driver"
  version = "1.4.8"
  namespace = "kube-system"
  set {
    name = "syncSecret.enabled"
    value = "true"
  }
}

resource "helm_release" "secrets_provider_aws" {
  name = "secrets-provider-aws"
  repository = "https://aws.github.io/secrets-store-csi-driver-provider-aws"
  chart = "secrets-store-csi-driver-provider-aws"
  version = "0.3.11"
  namespace = "kube-system"
}

data "aws_iam_policy_document" "secrets_csi_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"
    condition {
      test = "StringEquals"
      variable = "${module.eks.oidc_provider}:sub"
      values = ["system:serviceaccount:${var.namespace}:${local.service_account}"]
    }
    condition {
      test     = "StringEquals"
      variable = "${module.eks.oidc_provider}:aud"
      values   = ["sts.amazonaws.com"]
    }
    principals {
      identifiers = [module.eks.oidc_provider_arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role" "secrets_csi" {
  assume_role_policy = data.aws_iam_policy_document.secrets_csi_assume_role_policy.json
  name               = "secrets-csi-role"
}

resource "aws_iam_policy" "secrets_csi" {
  name = "secrets-csi-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ]
      Resource = ["${data.aws_secretsmanager_secret.secrets_csi.arn}"]
    }]
  })
}

resource "aws_iam_role_policy_attachment" "secrets_csi" {
  policy_arn = aws_iam_policy.secrets_csi.arn
  role       = aws_iam_role.secrets_csi.name
}

resource "kubernetes_service_account" "secrets_csi_sa" {
  metadata {
    name = local.service_account
    namespace = var.namespace
    labels = {
      "app.kubernetes.io/name"      = local.service_account
    }
    annotations = {
      "eks.amazonaws.com/role-arn"               = aws_iam_role.secrets_csi.arn
      "eks.amazonaws.com/sts-regional-endpoints" = "true"
    }
  }
}

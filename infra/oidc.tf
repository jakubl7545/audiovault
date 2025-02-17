resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com",]
}

data "aws_iam_policy_document" "oidc_provider_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github_actions.arn]
    }

    condition {
      test = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values = ["sts.amazonaws.com"]
    }

    condition {
      test = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values = ["repo:jakubl7545/audiovault:*"]
    }
  }
}

resource "aws_iam_role" "github_actions_ecr_access" {
  name = "github_actions_ecr_access"
  assume_role_policy = data.aws_iam_policy_document.oidc_provider_assume_role_policy.json
}

resource "aws_iam_policy_attachment" "ecr_access_attachment" {
  name = "ECR access attachment"
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
  roles = [aws_iam_role.github_actions_ecr_access.name]
}
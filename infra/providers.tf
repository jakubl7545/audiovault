terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
  required_version = "~> 1.3"
}

provider aws {
  region = "eu-north-1"
}

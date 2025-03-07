terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.83"
    }
  }
  required_version = "~> 1.3"
}

provider aws {
  region = var.region
}

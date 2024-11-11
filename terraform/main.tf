terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      Environment = var.environment
      Name = "provider"
  }
}
}

# Setting up AWS connection ^^^


terraform {
  backend "s3" {
    bucket = "espresso-state-bucket"
    key = "terraform.tfstate"
    region = "eu-west-2"
  }
}

# Setting up the S3 backend i.e. connecting the state bucket ^^^
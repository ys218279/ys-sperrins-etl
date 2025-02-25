terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3"{
    bucket = "sperrins-data-bucket"
    key = "tf_state/project_sperrins.tfstate"
    region = "eu-west-2"
    }
}
   

provider "aws" {
  region = "eu-west-2"
  default_tags {
  }
}

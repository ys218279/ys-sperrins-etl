data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

variable "ingestion_bucket_prefix" {
  description = "Value of the Name tag for the ingestion_bucket_prefix"
  type        = string
  default     = "ingestion-zone"

}

variable "Environment" {
  description = "The enviroment tag for AWS resources"
  type        = string
  default     = "dev"
}

variable "ingestion_lambda" {
  type    = string
  default = "ingestion_lambda"
}

variable "transform_lambda" {
  type    = string
  default = "transform_lambda"
}

variable "load_lambda" {
  type    = string
  default = "load_lambda"
}

variable "state_machine_scheduler" {
  type    = string
  default = "state_machine_scheduler"
}

variable "python_runtime" {
  type    = string
  default = "python3.12"
}

variable "default_timeout" {
  type    = number
  default = 20
}
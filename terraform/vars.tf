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

variable "state_machine" {
  type    = string
  default = "pipeline_state_machine"
}

variable "eventbridge_scheduler" {
  type    = string
  default = "eventbridge_scheduler"
}

variable "python_runtime" {
  type    = string
  default = "python3.12"
}

variable "default_timeout" {
  type    = number
  default = 20
}

variable "processed_bucket_prefix" {
  description = "Value of the Name tag for the processed_bucket_prefix"
  type        = string
  default     = "processed-zone"

}

variable "totesys_credentials_secret_name" {
  description = "Name of secret containing totesys db credentials"
  type = string
  default = "de_2024_12_02"
}

#INTERACTIVE VARIABLES
/* Whenever we create an interactive variable we have to use
the prefix letter to set the order of the interactive 
variables, interactive variables are called in alphabetical
order */

variable "a_totesys_username" {
  description = "Please enter your totesys DB username: "
  type = string
}

variable "b_totesys_password" {
  description = "Please enter your totesys DB password: "
  type = string
  sensitive = true
}

variable "c_totesys_host" {
  description = "Please enter your totesys DB host: "
  type = string
}

variable "d_totesys_database" {
  description = "Please enter your totesys database name : "
  type = string
}

variable "e_totesys_port" {
  description = "Please enter your totesys DB port: "
  type = string
}
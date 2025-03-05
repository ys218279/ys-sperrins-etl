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
  default = 60
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
  sensitive = true
}

variable "DW_credentials_secret_name" {
  description = "Name of secret containing final Data Warehouse db credentials"
  type = string
  default = "totesys_data_warehouse_olap"
  sensitive = true
}

variable "I_DB_PORT" {
  description = "Please enter your totesys DB port: "
  type = string
  default = 5432
}

#INTERACTIVE VARIABLES
/* Whenever we create an interactive variable we have to use
the prefix letter to set the order of the interactive 
variables, interactive variables are called in alphabetical
order */

variable "A_TOTESYS_USERNAME" {
  description = "Please enter your totesys DB username: "
  type = string
  sensitive = true
}

variable "B_TOTESYS_PASSWORD" {
  description = "Please enter your totesys DB password: "
  type = string
  sensitive = true
}

variable "C_TOTESYS_HOST" {
  description = "Please enter your totesys DB host: "
  type = string
  sensitive = true
}

variable "D_TOTESYS_DATABASE" {
  description = "Please enter your totesys database name : "
  type = string
}

variable "E_FINALDW_USERNAME" {
  description = "Please enter your totesys DB username: "
  type = string
  sensitive = true
}

variable "F_FINALDW_PASSWORD" {
  description = "Please enter your totesys DB password: "
  type = string
  sensitive = true
}

variable "G_FINALDW_HOST" {
  description = "Please enter your totesys DB host: "
  type = string
  sensitive = true
}

variable "H_FINALDW_DATABASE" {
  description = "Please enter your totesys database name : "
  type = string
}

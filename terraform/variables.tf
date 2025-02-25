
variable "ingestion_bucket_prefix" {
  description = "Value of the Name tag for the ingestion_bucket_prefix"
  type        = string
  default = "ingestion-zone"
  
}

variable "Environment" {
  description = "The enviroment tag for AWS resources"
  type        = string
  default = "dev"
}
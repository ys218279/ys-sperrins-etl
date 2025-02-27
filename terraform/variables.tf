
variable "ingestion_bucket_prefix" {
  description = "Value of the Name tag for the ingestion_bucket_prefix"
  type        = string
  default = "ingestion-zone"
  
}

variable "lambda_Ingestion_topic_name" {
  description = "Value of the Name tag for the lambda_Ingestion_topic_name"
  type        = string
  default = "Lambda_ingestion_topic"
  
}

variable "email_address" {
  description = "value of email used to subscribe to sns"
  //we are using a fake temp email service to set as a defualt email until we have one made for the project
  type        = string
  default = "rakoxi5744@btcours.com"
}

variable "Environment" {
  description = "The enviroment tag for AWS resources"
  type        = string
  default = "dev"
}
# Create an SNS topic
resource "aws_sns_topic" "lambda_Ingestion_topic" {
  name = var.lambda_Ingestion_topic_name 
}


#havent figured out names
resource "aws_sns_topic_subscription" "lambda_Ingestion_topic_target" {
  topic_arn = aws_sns_topic.lambda_Ingestion_topic.arn
  protocol  = "email"
  endpoint  = var.email_address
}
// run terraform first 
// sns topic -> subscribe
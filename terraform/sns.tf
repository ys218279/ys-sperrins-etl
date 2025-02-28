<<<<<<< HEAD
# Create an SNS topic
=======
>>>>>>> 925fced262a7eac4b50d5b3379f9dfaac6aa2047
resource "aws_sns_topic" "team_sperrins_topic" {
  name = var.lambda_ingestion_topic_name 
}


#havent figured out names
resource "aws_sns_topic_subscription" "team_sperrins_topic" {
  topic_arn = aws_sns_topic.team_sperrins_topic.arn
  protocol  = "email"
  endpoint  = var.email_address
}
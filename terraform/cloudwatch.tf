resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${var.ingestion_lambda}"
  retention_in_days = 14
}

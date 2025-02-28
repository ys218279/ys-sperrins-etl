resource "aws_cloudwatch_metric_alarm" "ingestion_lambda_alarm" {
  alarm_name          = "Ingestion-lambda-failure"
  alarm_description   = "Triggers when ingestion lambda fails."
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_actions       = [aws_sns_topic.team_sperrins_topic.arn]

  dimensions = {
    FunctionName = aws_lambda_function.ingestion_lambda.function_name
  }
}
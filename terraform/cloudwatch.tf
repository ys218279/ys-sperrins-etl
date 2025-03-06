resource "aws_cloudwatch_log_group" "ingestion" {
  name              = "/aws/lambda/${var.ingestion_lambda}"
}

resource "aws_cloudwatch_log_metric_filter" "ingestion_metric_filter"{
    name           = "Errors_for_ingestion_lambda"
  pattern        = "ERROR"
  log_group_name = aws_cloudwatch_log_group.ingestion.name

  metric_transformation {
    name      = "ingestion_lambda_errors"
    namespace = "ingestion_lambda"
    value     = "1"
  }
}


resource "aws_cloudwatch_metric_alarm" "ingestion_lambda_alarm" {
  alarm_name          = "Ingestion-lambda-failure"
  alarm_description   = "Triggers when ingestion lambda fails."
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.ingestion_metric_filter.metric_transformation[0].name
  namespace           = "ingestion_lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_actions       = [aws_sns_topic.team_sperrins_topic.arn]
}
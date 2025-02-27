
# eventbridge scheduler trigggers/invokes the stepfunction every 5(?) minutes
# the stepfunction invokes the first lambda (no payload entering?)
# the lambda runs and dumps to s3 (exit payload success message?)
# the payload from lambda 1 is passed to lambda 2 as payload, triggering lambda 2

resource "aws_sfn_state_machine" "pipeline_state_machine" {
  name     = "My-pipeline-statemachine-terraform-generated"
  role_arn = aws_iam_role.state_machine_role.arn
  definition = templatefile("${path.module}/mystatemachine.asl.json", {
    ProcessingLambda = "arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:function:${var.ingestion_lambda}:$LATEST"
    } 
  )
}


resource "aws_scheduler_schedule" "step_function_eventbridge" {
  name = "invoke-step-function-eventbridge"
  flexible_time_window {
    mode = "OFF"
  }
  schedule_expression = "rate(5 minute)"
  target {
    arn = aws_sfn_state_machine.pipeline_state_machine.arn
    role_arn = aws_iam_role.event_bridge_role.arn
  }
}
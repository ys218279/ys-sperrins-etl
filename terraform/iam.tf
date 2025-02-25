#iam assume policy 
data "aws_iam_policy_document" "lambda_ingestion_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# iam role
resource "aws_iam_role" "iam_role_for_lambda" {
 
  name_prefix        = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_ingestion_assume_role.json
}

# policy document for s3 bucket
data "aws_iam_policy_document" "ingestion_s3_policy" {
  statement {
    sid = "1"
    
    actions = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.ingestion_bucket.arn}/*"]    
  }
}

# policy for s3 ingestion bucket
resource "aws_iam_policy" "s3_policy" {
    name = "s3_policy"
    policy = data.aws_iam_policy_document.ingestion_s3_policy.json
  
}

# policy attachment to the role "iam_role_for_lambda"
resource "aws_iam_policy_attachment" "lambda_s3_policy_attachment" {
  name = "lambda-s3-policy-attachment"
  roles = [aws_iam_role.iam_role_for_lambda.name]
  policy_arn = aws_iam_policy.s3_policy.arn
}

/*
# ------------------------------
# Lambda IAM Policy for CloudWatch
# ------------------------------
*/


#Policy document for cloudwatch
data "aws_iam_policy_document" "cw_document" {
  statement {
        
    effect = "Allow"

    actions = [
      "logs:GetLogEvents",
      "logs:PutLogEvents"
    ]
     resources = ["arn:aws:logs:*:*:*"]
  }
    
    statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:DescribeLogStreams",
      "logs:PutRetentionPolicy",
      "logs:CreateLogGroup"
      
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

# Create policy with policy document defined above
resource "aws_iam_policy" "cloudwatch_policy" {
  
  name = "cloudwatch_policy"
  policy = data.aws_iam_policy_document.cw_document.json
}

# Attach the cw policy to the lambda role
resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
  role = aws_iam_role.iam_role_for_lambda.name
}


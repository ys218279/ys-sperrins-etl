# Initial IAM role set up

# Trust Policies for Lambda and State Machine
# Define
data "aws_iam_policy_document" "trust_policy_lambda" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "trust_policy_state_machine" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["states.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Roles

# Create
# Attach
resource "aws_iam_role" "ingestion_lambda_role" {
  name_prefix        = "role-${var.ingestion_lambda}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy_lambda.json
} 

resource "aws_iam_role" "transform_lambda_role" {
  name_prefix        = "role-${var.transform_lambda}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy_lambda.json
}

resource "aws_iam_role" "load_lambda_role" {
  name_prefix        = "role-${var.load_lambda}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy_lambda.json
}

resource "aws_iam_role" "state_machine_role" {
  name_prefix        = "general-state-machine-role"
  assume_role_policy = data.aws_iam_policy_document.trust_policy_state_machine.json
} 

# Please define the Data blocks for policy documents and 
# Create two Resource blocks:
    # One for creating the "aws_iam_policy" (uses the data block above) and 
    # One for attaching the "aws_iam_role_policy_attachment" to the roles created above


###S3 policies

# policy document for s3 bucket
data "aws_iam_policy_document" "ingestion_s3_policy" {
  statement {
    sid = "1"
    
    actions = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.ingestion_bucket.arn}/*"]    
  }
}

/*
# ------------------------------
# Lambda IAM Policy for S3-ingestion
# ------------------------------
*/


# policy for s3 ingestion bucket
resource "aws_iam_policy" "s3_policy" {
    name_prefix = "s3-policy-${var.ingestion_lambda}-write"
    
    policy = data.aws_iam_policy_document.ingestion_lambda_role.json
  
}

# policy attachment to the role "iam_role_for_lambda"
resource "aws_iam_policy_attachment" "lambda_s3_policy_attachment" {
  name = "lambda-s3-policy-attachment"
  roles = [aws_iam_role.ingestion_lambda_role.name]
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
  
  name_prefix = "cloudwatch-policy-${var.ingestion_lambda}-logging"
  policy = data.aws_iam_policy_document.cw_document.json
}

# Attach the cw policy to the lambda role
resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
  role = aws_iam_role.ingestion_lambda_role.name
}
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

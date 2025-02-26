

data "archive_file" "ingestion_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/ingestion_lambda/function.zip"
  source_dir = "${path.module}/../src/src_ingestion"
}

data "archive_file" "transform_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/transform_lambda/function.zip"
  source_dir = "${path.module}/../src/src_transform"
}

data "archive_file" "load_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/load_lambda/function.zip"
  source_dir = "${path.module}/../src/src_load"
}

resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = "team-09-amazing-code-"
}


resource "aws_s3_object" "lambda_code" {
  for_each = toset([var.ingestion_lambda, var.transform_lambda, var.load_lambda])
  bucket   = aws_s3_bucket.code_bucket.bucket
  key      = "${each.key}/function.zip"
  source   = "${path.module}/../packages/${each.key}/function.zip"
  etag     = filemd5("${path.module}/../packages/${each.key}/function.zip")
}


resource "aws_lambda_function" "ingestion_lambda" {
  function_name    = var.ingestion_lambda
  source_code_hash = data.archive_file.ingestion_lambda.output_base64sha256
  s3_bucket        = aws_s3_bucket.code_bucket.bucket
  s3_key           = "${var.ingestion_lambda}/function.zip"
  role             = aws_iam_role.ingestion_lambda_role.arn
  handler          = "${var.ingestion_lambda}.lambda_handler"
  runtime          = var.python_runtime
  timeout          = var.default_timeout
#   layers           = [aws_lambda_layer_version.dependencies.arn]

#   depends_on = [aws_s3_object.lambda_code, aws_s3_object.lambda_layer]
   depends_on = [ aws_s3_object.lambda_code ]
}

resource "aws_lambda_function" "transform_lambda" {
  function_name    = var.transform_lambda
  source_code_hash = data.archive_file.transform_lambda.output_base64sha256
  s3_bucket        = aws_s3_bucket.code_bucket.bucket
  s3_key           = "${var.transform_lambda}/function.zip"
  role             = aws_iam_role.transform_lambda_role.arn
  handler          = "${var.transform_lambda}.lambda_handler"
  runtime          = var.python_runtime
  timeout          = var.default_timeout
#   layers           = [aws_lambda_layer_version.dependencies.arn]

#   depends_on = [aws_s3_object.lambda_code, aws_s3_object.lambda_layer]
   depends_on = [ aws_s3_object.lambda_code ]
}

resource "aws_lambda_function" "load_lambda" {
  function_name    = var.load_lambda
  source_code_hash = data.archive_file.load_lambda.output_base64sha256
  s3_bucket        = aws_s3_bucket.code_bucket.bucket
  s3_key           = "${var.load_lambda}/function.zip"
  role             = aws_iam_role.load_lambda_role.arn
  handler          = "${var.load_lambda}.lambda_handler"
  runtime          = var.python_runtime
  timeout          = var.default_timeout
#   layers           = [aws_lambda_layer_version.dependencies.arn]

#   depends_on = [aws_s3_object.lambda_code, aws_s3_object.lambda_layer]
   depends_on = [ aws_s3_object.lambda_code ]
}
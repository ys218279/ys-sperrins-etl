resource "aws_secretsmanager_secret" "totesys_secret" {
  name = var.totesys_credentials_secret_name
}

resource "aws_secretsmanager_secret_version" "totesys_secret_version" {
  secret_id     = aws_secretsmanager_secret.totesys_secret.id
  secret_string = jsonencode({ username = var.a_totesys_username 
  password = var.b_totesys_password 
  host = var.c_totesys_host 
  database = var.d_totesys_database 
  port = var.e_totesys_port })
}


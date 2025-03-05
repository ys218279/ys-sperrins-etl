resource "aws_secretsmanager_secret" "totesys_secret" {
  name = var.totesys_credentials_secret_name
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "totesys_secret_version" {
  secret_id     = aws_secretsmanager_secret.totesys_secret.id
  secret_string = jsonencode({ username = var.A_TOTESYS_USERNAME 
  password = var.B_TOTESYS_PASSWORD 
  host = var.C_TOTESYS_HOST 
  database = var.D_TOTESYS_DATABASE 
  port = var.I_DB_PORT })
}

resource "aws_secretsmanager_secret" "Data_Warehouse_secret" {
  name = var.DW_credentials_secret_name
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "finalDW_secret_version" {
  secret_id     = aws_secretsmanager_secret.Data_Warehouse_secret.id
  secret_string = jsonencode({  username = var.E_FINALDW_USERNAME 
                                password = var.F_FINALDW_PASSWORD 
                                host = var.G_FINALDW_HOST 
                                database = var.H_FINALDW_DATABASE 
                                port = var.I_DB_PORT })
}
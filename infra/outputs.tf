output "db_endpoint" {
  description = "rds db endpoint"
  value = aws_db_instance.audiovault_rds.endpoint
}

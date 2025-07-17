output "db_endpoint" {
  description = "rds db endpoint"
  value = aws_db_instance.audiovault_rds.endpoint
}

output "efs_id" {
  description = "EFS file system id"
value = aws_efs_file_system.audiovault_efs.id
}
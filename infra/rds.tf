resource "aws_security_group" "audiovault_rds_sg" {
  name = "audiovault_rds_sg"
  description = "Allow access for RDS Database on Port 3306"
  vpc_id = module.vpc.vpc_id
  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
}

resource "aws_db_instance" "audiovault_rds" {
  engine = "mariadb"
  engine_version = "11.4"
  db_name = "audiovault"
  identifier = "audiovault"
  instance_class = "db.t3.micro"
  allocated_storage = 10
  publicly_accessible = false
  username = jsondecode(data.aws_secretsmanager_secret_version.current.secret_string)["db_user"]
password = jsondecode(data.aws_secretsmanager_secret_version.current.secret_string)["db_password"]
  vpc_security_group_ids = [aws_security_group.audiovault_rds_sg.id]
  skip_final_snapshot = true
  db_subnet_group_name = module.vpc.database_subnet_group_name
  multi_az = true
}
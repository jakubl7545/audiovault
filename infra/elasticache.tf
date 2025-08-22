resource "aws_security_group" "audiovault_elasticache_sg" {
  name = "audiovault_elasticache_sg"
  description = "Allow access for Elasticache cluster on Port 11211"
  vpc_id = module.vpc.vpc_id
  ingress {
    from_port = 11211
    to_port = 11211
    protocol = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
}

resource "aws_elasticache_cluster" "audiovault_elasticache" {
  cluster_id = "audiovault-elasticache"
  engine = "memcached"
  engine_version = "1.6.22"
  node_type = "cache.t3.small"
  num_cache_nodes = 2
  parameter_group_name = "default.memcached1.6"
  port = 11211
  security_group_ids = [aws_security_group.audiovault_elasticache_sg.id]
  subnet_group_name = module.vpc.elasticache_subnet_group_name
}

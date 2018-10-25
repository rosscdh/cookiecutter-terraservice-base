module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "1.46.0"

  name = "${var.name}"
  cidr = "${var.cidr}"

  azs             = "${var.azs}"
  private_subnets = "${var.private_subnets}"
  public_subnets  = "${var.public_subnets}"

  enable_nat_gateway = "${var.enable_nat_gateway}"

  tags = {
    Terraform = "true"
    Environment = "${var.tag_environment}"
  }
}

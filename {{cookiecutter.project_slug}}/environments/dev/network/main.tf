#
# Docs https://vorwerk.atlassian.net/wiki/spaces/NWOT/pages/323224585/Network+Design+for+NWOT
#
terraform {
  backend "s3" {
    bucket = "test-ti-dev-{{cookiecutter.project_slug}}"
    key    = "terraform/{{cookiecutter.project_slug}}/dev/network"
    region = "eu-central-1"
  }
}

data "terraform_remote_state" "network" {
  backend = "s3"
  config {
    bucket = "test-ti-dev-{{cookiecutter.project_slug}}"
    key    = "terraform/{{cookiecutter.project_slug}}/dev/network/terraform.tfstate"
    region = "eu-central-1"
  }
}

#
# https://vorwerk.atlassian.net/wiki/spaces/NWOT/pages/323224585/Network+Design+for+NWOT
#
module "network" {
  source                = "../../../layers/network"
    name                = "ti-main"
    cidr                = "10.1.0.0/16"
    azs                 = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]
    private_subnets     = [
            # Openshift
            "10.1.0.0/19", "10.1.32.0/19", "10.1.64.0/19"
            # Technical Infrastructure 
    ]
    public_subnets      = ["10.208.0.0/20", "10.208.16.0/20", "10.208.32.0/20"] # Openshift Public Networks??
    enable_nat_gateway  = true
    tag_environment     = "dev"
}


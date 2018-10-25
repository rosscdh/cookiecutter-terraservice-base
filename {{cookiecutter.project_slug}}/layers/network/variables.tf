variable "name" {
    description = ""
}
variable "cidr" {
    description = ""
}
variable "azs" {
    type        = "list"
    description = ""
    default     = []
}
variable "private_subnets" {
    type        = "list"
    description = ""
}
variable "public_subnets" {
    type        = "list"
    description = ""
}
variable "enable_nat_gateway" {
    description = ""
    default = "true"
}
variable "tag_environment" {
    description = ""
}
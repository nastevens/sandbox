variable "shard_name" {
    description = "Name env and region concatenated together"
}

variable "vpc_name" {
    description = "The unique VPC name this module is being instantiated into"
}

variable "vpc_id" {
    description = "The unique VPC ID this module is being instantiated into"
}

variable "public_subnets" {
    description = "A comma-delimited list of public subnets for the VPC"
}

variable "datadog_enabled" {
    description = "Should datadog be monitoring this environment (true|false)"
}

variable "billing_tag" {
    description = "The AWS tag used to track AWS charges"
}

variable "ssl_certificate_id" {
    description = "The ARN of the SSL certificate to use for this server's ELB"
}

variable "updaterng_s3_bucket" {
    description = "The name of the bucket containing firmware updates to serve"
}

module "updaterng" {
    source = "./updaterng"
    shard_name = "global"
    vpc_name = "basic_vpc"
    vpc_id = "vpc-3ca9645a"
    public_subnets = "subnet-501f6019"
    datadog_enabled = false
    billing_tag = "none"
    ssl_certificate_id = "arn:aws:acm:us-east-1:176959676258:certificate/690758e2-fb81-4fe3-bb54-662d6f8ff9a6"
    updaterng_s3_bucket = "smartthings-updaterng-sandbox"
}

resource "aws_s3_bucket" "update_bucket" {
    bucket = "bitcurry-updaterng-sandbox"
    acl    = "private"
    versioning {
        enabled = false
    }
    tags {
        Name = "bitcurry-updaterng-sandbox"
    }
}

resource "aws_key_pair" "nick-test" {
    key_name = "nick-test"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC08SakppvOXyTHn3J+7AyuF0OBKekkXuGXv9Ga2JfwUZ7JPhvEiC1wJUHhtiFkriA/aozSeGV7uwJOGLaJ5Xq9h14AMfpbJoDzaCs5WuEwQWUyFhtFxV1NxDcx4PsjdQLDkLwEhGRups+sFB4xA0tE3djKisgm9OuxWybFmYyPumfjyq2icC32nvlNlBYGvPmMN5PoXM72E/qBc79aR0MhbWCumsERgmkcFGcsvIsLiLmVsFgYh7jqyyOR5Zi27ofOJGqYMWN+Vq4IYbTzacV4Uf+9l+pkdOG5QilA9Nwno6b6ezb6H1IWYJkrk49yUelv28Lm24Ujwxb32eN4Z5L1kL7IJxH8cD02hf0UIJ5VXByzMULnbi/FbDLwKchNtO5WrS5ExNooJyB8EY1DIzQUKYVqb1cohvNo4HRQOsrKkgzi2w4ZEAVQ73+nIR9AdL2ygVkKMuMs93uzkI+2Wd/LlYv5/4ZWLl32o/cxNYiftnY2pJJo+lheyECPHMlM7W9+qiyIqW2cXGXe2tMJIxdg9afgg422KJQ6E4bKr7WMGW74/5YCImsb1ATPUmE7sjYlkxoJOxc/+JKLHrVp63wADv/3RpCp5jBhuHbaJjBcDA/TpWBFMDomgrtVsF95jz51oO9AstIR7/5MueQcL15XScaRxV8LWSKfdgMuZ+lDEQ== nick.stevens@smartthings.com"
}

resource "aws_security_group" "ext_ssh" {
  name = "ext-ssh"
  description = "updaterng SSH access"
  vpc_id = "vpc-3ca9645a"

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [ "0.0.0.0/0" ]
  }
}

resource "aws_instance" "example" {
    ami = "ami-fce3c696"
    instance_type = "t2.micro"
    key_name = "nick-test"
    subnet_id = "subnet-501f6019"
    iam_instance_profile = "${module.updaterng.updaterng_instance_profile}"
    associate_public_ip_address = true
    vpc_security_group_ids = [
        "${module.updaterng.server_sg_id}",
        "${aws_security_group.ext_ssh.id}"
    ]
}

resource "aws_elb_attachment" "updaterng_elb_instance_attachment" {
    elb = "${module.updaterng.elb_id}"
    instance = "${aws_instance.example.id}"
}

provider "aws" {
    region                  = "us-east-1"
    shared_credentials_file = "/Users/nick/.aws/credentials"
    profile                 = "personal"
}

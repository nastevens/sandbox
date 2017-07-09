resource "aws_iam_role" "app_updaterng" {
    name = "app-updaterng"
    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [ {
        "Action": "sts:AssumeRole",
        "Principal": {
            "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
    } ]
}
EOF
}

resource "aws_iam_role_policy" "app_updaterng_s3" {
    name = "updaterng-s3-artifact-download"
    role = "${aws_iam_role.app_updaterng.id}"
    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [ {
        "Effect": "Allow",
        "Action": [ "s3:ListBucket" ],
        "Resource": [ "arn:aws:s3:::${var.updaterng_s3_bucket}" ]
    },
    {
        "Effect": "Allow",
        "Action": [ "s3:GetObject" ],
        "Resource": [ "arn:aws:s3:::${var.updaterng_s3_bucket}/*" ]
    } ]
}
EOF
}

resource "aws_iam_instance_profile" "app_updaterng" {
    name  = "app-updaterng-profile"
    roles = [ "${aws_iam_role.app_updaterng.name}" ]
}

resource "aws_security_group" "updaterng_ext_lb" {
  name = "updaterng-${var.vpc_name}-ext"
  description = "updaterng ELB Security Group"
  vpc_id = "${var.vpc_id}"

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  ingress {
    from_port = 11111
    to_port = 11111
    protocol = "tcp"
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  tags {
    Name = "updaterng-${var.vpc_name}-ext"
  }
}

resource "aws_security_group" "updaterng" {
  name = "updaterng-${var.vpc_name}"
  description = "updaterng Instance Security Group"
  vpc_id = "${var.vpc_id}"

  ingress {
    from_port = 11111
    to_port = 11111
    protocol = "tcp"
    security_groups = [ "${aws_security_group.updaterng_ext_lb.id}" ]
  }

  ingress {
    from_port = 11112
    to_port = 11112
    protocol = "tcp"
    security_groups = [ "${aws_security_group.updaterng_ext_lb.id}" ]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  tags {
    Name = "updaterng-${var.vpc_name}"
  }
}

resource "aws_elb" "updaterng_ext" {
  name = "updaterng-${var.shard_name}-ext"
  subnets = [ "${split(",", var.public_subnets)}" ]
  internal = false
  security_groups = [ "${aws_security_group.updaterng_ext_lb.id}" ]

  cross_zone_load_balancing = true
  idle_timeout = 60
  connection_draining = true

  listener {
    lb_protocol = "ssl"
    lb_port = "443"
    instance_protocol = "tcp"
    instance_port = "11111"
    ssl_certificate_id = "${var.ssl_certificate_id}"
  }

  listener {
    lb_protocol = "ssl"
    lb_port = "11111"
    instance_protocol = "tcp"
    instance_port = "11111"
    ssl_certificate_id = "${var.ssl_certificate_id}"
  }

  health_check {
    healthy_threshold = 3
    unhealthy_threshold = 2
    timeout = 5
    interval = 10
    target = "HTTP:11112/status"
  }

  tags {
    Name = "updaterng-${var.vpc_name}-ext"
    datadog_monitor = "${var.datadog_enabled}"
    billing = "${var.billing_tag}"
  }
}

/*
resource "aws_route53_record" "updaterng_ext_dns" {
   zone_id = "${var.public_r53_zone_id}"
   name = "fw-update2"
   type = "A"
   region = "${var.aws_region}"
   set_identifier = "${var.aws_region}"
   alias {
      name = "${aws_elb.updaterng_ext.dns_name}"
      zone_id = "${aws_elb.updaterng_ext.zone_id}"
      evaluate_target_health = true
   }
}
*/

output "server_sg_id" {
    value = "${aws_security_group.updaterng.id}"
}

output "elb_id" {
    value = "${aws_elb.updaterng_ext.id}"
}

output "updaterng_instance_profile" {
    value = "${aws_iam_instance_profile.app_updaterng.id}"
}

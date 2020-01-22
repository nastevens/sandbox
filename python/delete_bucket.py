#!/usr/bin/env python3

BUCKET = "st-firmware-jenkins-master-backup"

import boto3
import itertools
import sys

total = 0
s3 = boto3.client("s3")
paginator = s3.get_paginator('list_object_versions')
for page in paginator.paginate(Bucket=BUCKET):
    to_delete = [
        {"Key": version["Key"], "VersionId": version["VersionId"]}
        for version in itertools.chain(page["Versions"], page["DeleteMarkers"])
    ]

    s3.delete_objects(Bucket=BUCKET,
        Delete={
            "Objects": to_delete,
            "Quiet": True,
        }
    )
    total += len(to_delete)
    print(total)

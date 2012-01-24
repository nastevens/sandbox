#!/bin/bash

rsync -av --delete --delete-excluded /mnt/kingston/. /common/backup/kingston_backup/

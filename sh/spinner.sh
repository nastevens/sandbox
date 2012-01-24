#!/bin/sh

while true; do
    for c in \| \/ \- \\; do
        echo -n "\r$c"
        sleep 1
    done
done

#!/bin/sh

# video track (pass: 1, bitrate: 1000)
nice -n 3 mencoder -sws 2 -nosound -ovc lavc \
 -lavcopts vcodec=mpeg4:vbitrate=1400:vhq:vpass=1:turbo \
 -ffourcc XVID  -dvd-device /dev/hdd dvd://1 -o /dev/null \
 -vf crop=704:464:8:6

# video track (pass: 2, bitrate: 1000)
nice -n 3 mencoder -sws 2 -oac copy -ovc lavc \
 -lavcopts vcodec=mpeg4:vbitrate=1400:vhq:vpass=2 \
 -ffourcc XVID  -dvd-device /dev/hdd -aid 128 dvd://1 -o "Ice Age - The Meltdown.avi" \
 -vf crop=704:464:8:6

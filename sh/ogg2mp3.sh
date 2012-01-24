#!/bin/sh

for var in "$@"
do
  mplayer -ao pcm "$var"
  lame -h -b 160 audiodump.wav "$var.mp3"
done

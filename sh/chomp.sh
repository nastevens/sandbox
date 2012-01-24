#!/bin/sh

for i in *.flac; do 
  track=`echo "$i" | gawk -F '-' '{print $1}' | sed 's/^ *//;s/ *$//;s/.flac//g'`
  artist=`echo "$i" | gawk -F '-' '{print $2}' | sed 's/^ *//;s/ *$//;s/.flac//g'`
  name=`echo "$i" | gawk -F '-' '{print $3}' | sed 's/^ *//;s/ *$//;s/.flac//g'`

  metaflac --set-tag="artist=$artist" --set-tag="album=Kong in Concert" --set-tag="title=$name" --set-tag="tracknumber=$track" "$i"
done

#!/bin/sh
# May need to exclude Aplus if it keeps causing problems

START=1937
END=2017
BASEURL='http://www.ocremix.org/remix/OCR0'

for (( i = $START; i <= $END; i++ ))
do
	# Steps:
	# 1) wget fetches index of file
	# 2) grep pulls out the mp3 filename
	# 3) sed extracts just the mp3 URLs
	MP3URLS=`wget -q -O - "$BASEURL$i/" | grep '\.mp3' | sed 's/.*"\(.*\)".*/\1/g'`
	
	# Count the number of URLs we retrieved
	URLCOUNT=`echo "$MP3URLS" | wc -l`

	# Distribute amongst the different mirrors
	MP3URL=`echo "$MP3URLS" | sed -n "\`expr $i % ${URLCOUNT} + 1\`p"`

	echo "Getting OCR #$i: $MP3URL"
	wget -nv "$MP3URL"
done

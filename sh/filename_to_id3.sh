for i in *; do id3tag -2 -t `echo "${i}" | gawk '{ print $1 }'` -s "`echo "${i}" | gawk -F - '{ print $2 }' | sed -e 's/^ *//g;s/.mp3//g'`" "${i}"; done

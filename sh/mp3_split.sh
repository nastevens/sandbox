#!/bin/sh

FRAMES=24000
CHUNKS=70

for (( i=0; $i<$CHUNKS; i++ ))
do
  let start=$i*$FRAMES
  let end=($i+1)*$FRAMES

  if (( $i<10 ))
  then
    file="0$i-HP3"
  else
    file="$i-HP3"
  fi  
  
  mpg321 -k $start -n $end -s J.\ K.\ Rowling\ -\ Harry\ Potter\ And\ The\ Prisioner\ Of\ Azkaban.mp3 | lame -r -s 44.1 -b 32 -m s -x - $file.mp3
done

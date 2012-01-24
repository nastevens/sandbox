#!/bin/sh

export USER=printsniper

if [ -f "/home/nick/.MTcount" ]
then
  curpage=`cat /home/nick/.MTcount`
else
  echo "No starting point found"
fi 

if [ "$2" != "" ]
then
  printer=$2
else
  printer="Skinner"
fi  

i=$curpage
status="Status messages:"
fpath="/home/nick/Megatokyo/"

for (( i; i < `expr $curpage + 10`; i++))
do

  if [ $i -lt 10 ]
  then
    filenumber="000$i"
    
  elif [ $i -lt 100 -a $i -ge 10 ]
  then
    filenumber="00$i"
 
  elif [ $i -lt 1000 -a $i -ge 100 ]
  then
    filenumber="0$i"
 
  else
    status="$status Filenumber exceeds program specs"
  fi
  
  echo "PrintSniper printing file:$filenumber"

  # See if the file is a gif
  if [ -f "$fpath$filenumber.gif" ]
  then
    
    # Convert gif to PS
    /usr/local/bin/gif2ps $fpath$filenumber.gif > $fpath$filenumber.ps
    
    # Print file
    arg=$1
    if [ "$arg" = "ok" ]
    then
      /usr/bin/lpr -r -l -P $printer $fpath$filenumber.ps
      echo "GIF $filenumber  printed"
      status="$status GIF $filenumber printed"
    else
      echo "GIF $filenumber NOT printed"
      status="$status GIF $filenumber NOT printed"
    fi  

  elif [ -f "$fpath$filenumber.jpg" ]
  then
   
    # Convert jpeg to PS
    /usr/local/bin/jpeg2ps $fpath$filenumber.jpg > $fpath$filenumber.eps
    
    # Print file
    arg=$1
    if [ "$arg" = "ok" ]
    then
      /usr/bin/lpr -r -l -P $printer  $fpath$filenumber.eps
      echo "JPEG $filenumber printed"
      status="$status JPEG $filenumber printed "
    else
      echo "JPEG $filenumber NOT printed"
      status="$status JPEG $filenumber NOT printed"
    fi  
  
  else
    echo "Could not read file #$filenumber" 
    status="$status Error: Could not read file $filenumber" 
  fi  

done  

# Email results
echo "Subject: PrintSniper files $curpage to `expr $curpage + 9` printedThis message is to alert you that files $curpage to `expr $curpage + 9` have been printed to $printer and can be picked up.$status" | /var/qmail/bin/qmail-inject nick@toukon.net

# Update count
echo `expr $curpage + 10` | cat > /home/nick/.MTcount

# Done

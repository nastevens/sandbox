for i in *; do mv "$i" "${i}`id3info "$i" | grep Track | sed 's/=== TRCK (Track number\/Position in set): //g'`.mp3"; done; mmv '* - *.mp3*.mp3' '#3 - #2.mp3'; mmv '? - *' '0#1 - #2'

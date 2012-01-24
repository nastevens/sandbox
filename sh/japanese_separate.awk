{
    hira = $1;
    printf "%s:",hira;

    match($0,/\[.*\]/);
    if(RSTART != 0) {
        kanji = substr($0,RSTART+1,RLENGTH-2);
        printf "%s:",kanji;
    } else {
        printf ":";
    }

    match($0,/\/.*\//);
    if(RSTART != 0) {
        def = substr($0,RSTART+1,RLENGTH-2);
        printf "%s\n",def;
    } else {
        print "\n";
    }

}

for i in *; do mv "$i" "`basename \"$i\" .flac` [`metaflac --show-tag=artist \"$i\" | sed 's/artist=//g'`].flac"; done

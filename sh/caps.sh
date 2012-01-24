 for file in *; do out=""; for i in $file; do B=`echo -n "${i:0:1}" | tr '[:lower:]' '[:upper:]'`; out="${out} ${B}${i:1}"; done; mv "${file}" "${out}"; done && mmv ' *' '#1'

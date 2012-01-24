#!/usr/bin/gawk -f

BEGIN	{ FS="\t"; }
$0 !~ /NI_UnitTestFramework/ { 
	refnum = gensub(/.*(0x[[:xdigit:]]+).*/,"\\1","");
	type = gensub(/^.* (.*)$/,"\\1","",$4);
	vi = $3;
	if ($4 ~ /Obtain/ ) {
		count[refnum]++;
		obtained[refnum] = vi; 
		types[refnum] = type;
	}
	if ($4 ~ /Release/ ) {
		count[refnum]++;
		released[refnum] = vi;
	}

}
END 	{
	for (refnum in count) {
		total++;
		if (count[refnum] != 2 && count[refnum] != 0) {
			print types[refnum], refnum, "obtained in", obtained[refnum];
			unclosed++;
		}
	}
	print "Found", unclosed, "unclosed references in", total, "refs total";
}

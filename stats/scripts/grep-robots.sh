#!/bin/bash

output=$1

# Intermediate files
grep1=grep-all.txt
grep2=grep-domains.txt

if [ -f $grep1 ] ; then
    rm $grep1
fi

for f in logs/*.o*; do
    if [[ "$f" == logs/ce-* ]] 
    then
	echo "Command: grep -i 'robots.txt' $f >> $grep1"
	grep -i robots.txt $f >> $grep1
    fi
done

echo "Writing domains... "
sed -n -e 's/^.*robots.txt: //p' $grep1 | awk -F/ '{print $3}' > $grep2

echo "Removing duplicates..."
sort $grep2 | uniq -u > $output

rm $grep2

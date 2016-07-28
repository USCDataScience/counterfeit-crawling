counter=0
for d in wrangler/crawl-*/segments/*; do
    echo "Command: nutch/runtime/local/bin/nutch readseg -dump $d segments-dump/part-$counter -nocontent -nogenerate -noparse -noparsedata -noparsetext"
    nutch/runtime/local/bin/nutch readseg -dump $d segments-dump/part-$counter -nocontent -nogenerate -noparse -noparsedata -noparsetext
    counter=$((counter+1))
done
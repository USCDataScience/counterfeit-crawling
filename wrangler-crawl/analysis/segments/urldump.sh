CRAWL_DIR=$1

for x in `ls ${CRAWL_DIR}/segments`; 
do /work/04180/tg834792/wrangler/workspace/crawl-evaluation/workspace/nutch/runtime/local/bin/nutch readseg -dump ${CRAWL_DIR}/segments/${x} urldump/${x} -nocontent -nogenerate -noparse -noparsetext -noparsedata; done

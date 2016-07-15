for d in wrangler/*/; do
    echo "Command: nutch/runtime/local/bin/nutch dump -segment $d/segments -outputDir dump"
    nutch/runtime/local/bin/nutch dump -segment $d/segments -outputDir dump
done
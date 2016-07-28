Nutch Crawling of Counterfeit Electronics Seed Sites
===============================================================

Author: Joey Hong


1: Configuration
-------------------------------------------
Added rotating agent ID, made changes to Nutch configuration for politeness and 
whitelist, as well as URL filtering from only host seeded sites.

Set URL filters to accept image MIME extensions.

Changed Nutch to run in single-threaded fetching to support Selenium plugin. Edited
parameters in Nutch crawl script to single node.


2: Nutchpy (Deprecated)
-------------------------------------------
Wrote Nutchpy script to generate crawl statistics on crawldb dumps, scanning MIME types, 
and finding failed URLS. 

Wrote script to search through hadoop.log and find failed URLs with reason.


3: Nutch-Python and Crawl Client
-------------------------------------------
Used Nutch-Python to perform crawls using Nutch REST server.

Updating generating crawl statistics to use Nutch-Python and REST API instead of 
the Nutchpy library.


4: Selenium Handlers
------------------------------------------
Wrote a custom Selenium handler for the protocol-interactiveselenium Nutch plugin, 
which assists in focused crawling of relevant data.


5: Image Scripts
-----------------------------------------
Created scripts to get image URLS from crawldb, and also download them into a images 
directory.

Wrote script to extract image metadata by reading segments directory.


5.5: Tika-Python and Image Parsing 
------------------------------------------
Added function to normalize image pixels to grayscale, and return a string of grayscale
pixels representing image content. Used function with tika parser to create a metadata 
hash of an image by reading direction of image files.


6: Deduplication
------------------------------------------
Takes the output of image metadata extraction scripts and runs exact or near deduplication 
on the images using their metadata. 

Near deduplication uses the minhashing algorithm for locality-sensitive hashing on all the 
images' parsed metadata, whereas exact duplicates merely compute a hash of the image bytes.

Added an implementation of simhashing for near deduplication, which will work better for 
large datasets.


7: Scoring Similarity
------------------------------------------
Incorporated plugin that uses cosine distance from a goldstandard to score how relevant a page 
is to the desired content.


8: D3 Visualization
------------------------------------------
Used Tika-Similarity to compute edit distances between extracted images based on metadata, 
and D3 to visualize data in clusters. 

Resource: https://github.com/chrismattmann/tika-similarity


9: Wrangler Crawl
-------------------------------------------
Adapted crawls for the Wrangler supercomputer, including regular and hadoop runs over a larger
seed list. Custom selenium handlers and test with Ghostdriver for headless and parallelizable
web crawling with sites with Javascript.

Link: https://memexproxy.com/wiki/display/MEM/Counterfeit+Electronics+Crawl


9: Solr Indexing
-------------------------------------------
Indexed the crawled data on Apache Solr to allow queries. Atomic updates to the parsed pages
including titles, outlinks, aggregated dates, and extracted serial numbers from Tesseract OCR.


10: Summary Statistics
--------------------------------------------
Generate summary statistics for all the Wrangler crawls, update the statistics to the MEMEX
wiki page.

Link: https://memexproxy.com/wiki/display/MEM/Counterfeit+Electronics+Statistics
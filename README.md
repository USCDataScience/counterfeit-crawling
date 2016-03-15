Nutch Crawling of Counterfeit Electronics Seed Sites
===============================================================

Author: Joey Hong


Part 1: Configuration
-------------------------------------------
Added rotating agent ID, made changes to Nutch configuration for politeness and 
whitelist, as well as URL filtering from only host seeded sites.

Set URL filters to accept image MIME extensions.


Part 2: Nutchpy
-------------------------------------------
Wrote Nutchpy script to generate crawl statistics on crawldb dumps, scanning MIME types, 
and finding failed URLS. 


Part 3: Nutch-Python
-------------------------------------------
Used Nutch-Python to perform crawls using Nutch REST server.

Updating generating crawl statistics to use Nutch-Python and REST API instead of 
the Nutchpy library.

Created scripts to get image URLS from crawldb, and also download them into a images 
directory.
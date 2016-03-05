Nutch Crawling of Counterfeit Electronics Seed Sites
===============================================================

Author: Joey Hong


Part 1: Configuration
-------------------------------------------
Added rotating agent ID, made changes to Nutch configuration for politeness and 
whitelist, as well as URL filtering.


Part 2: Nutchpy
-------------------------------------------
Wrote Nutchpy script to generate crawl statistics on crawldb dumps, scanning MIME types, 
and finding failed URLS. 


Part 3: Nutch-Python
-------------------------------------------
Used Nutch-Python to perform crawls using Nutch REST server.
Nutch Crawling of Counterfeit Electronics Seed Sites
===============================================================

Author: Joey Hong


Part 1: Configuration
-------------------------------------------
Added rotating agent ID, made changes to Nutch configuration for politeness and 
whitelist, as well as URL filtering from only host seeded sites.

Set URL filters to accept image MIME extensions.

Changed Nutch to run in single-threaded fetching to suppor Selenium plugin.


Part 2: Nutchpy and Report Generation
-------------------------------------------
Wrote Nutchpy script to generate crawl statistics on crawldb dumps, scanning MIME types, 
and finding failed URLS. 

Wrote script to search through hadoop.log and find failed URLs with reason.


Part 3: Nutch-Python and Crawl Client
-------------------------------------------
Used Nutch-Python to perform crawls using Nutch REST server.

Updating generating crawl statistics to use Nutch-Python and REST API instead of 
the Nutchpy library.


Part 4: Selenium Handlers
------------------------------------------
Wrote a custom Selenium handler for the protocol-interactiveselenium Nutch plugin, 
which assists in focused crawling of relevant data.


Part 5: Image Scripts
-----------------------------------------
Created scripts to get image URLS from crawldb, and also download them into a images 
directory.

Also, wrote script to extract image metadata. 
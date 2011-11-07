RSParly Scrapers
================

This is a [Scrapy](http://scrapy.org/) project collecting together the three scrapers I put together for various
projects at [RSParly 2011](http://rewiredstate.org/events/parliament).

 - bills
 - committees
 - papers

Run the spiders
===============

In order to run the spiders you need to have Scrapy installed. Check out the project and run scrapy's 'crawl'
command from the root directory.

    > scrapy crawl bills

There is no explicit output defined so if you'd like the result written to a file but don't want to write your own
then you can use scrapy's built in [feed exports](http://readthedocs.org/docs/scrapy/en/latest/topics/feed-exports.html).

The following will produce a file called `bills.json` with one json object per line, suitable for importing into
MongoDB.

    > scrapy crawl bills --set FEED_URI=bills.json --set FEED_FORMAT=jsonlines

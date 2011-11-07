import urlparse
from scrapy.http.request import Request

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from RSParlyScrapers.items import CommitteeItem

class CommitteesSpider(CrawlSpider):
    name = 'committees'
    allowed_domains = ['parliament.uk']
    start_urls = ['http://www.parliament.uk/business/committees/committees-a-z/']

    def parse(self, response):
        return self.parse_list(response)

    def parse_list(self, response):
        hxs = HtmlXPathSelector(response)
        for href in hxs.select(r'//ul[@class="square-bullets-a-to-z"]//a/@href').extract():
            url = urlparse.urljoin(response.url, href)
            url = urlparse.urljoin(url, "membership")
            yield Request(url, callback=self.parse_members)

    def parse_members(self, response):
        committee = CommitteeItem()
        hxs = HtmlXPathSelector(response)

        committee['url'] = response.url
        committee['name'] = "".join(hxs.select(r'//h1/text()').extract()).strip()
        committee['members'] = hxs.select(r'//table[@class="members"]//tr/td[1]/a/text()').extract()

        return [committee]

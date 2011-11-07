from datetime import datetime
import re
import urlparse

from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
import time

from RSParlyScrapers.items import ResearchPaperItem

class PapersSpider(CrawlSpider):
    name = 'papers'
    allowed_domains = ['parliament.uk']
    start_urls = ['http://www.parliament.uk/business/publications/research/briefing-papers/']

    def parse(self, response):
        return self.parse_list(response)

    def parse_list(self, response):
        hxs = HtmlXPathSelector(response)
        for href in hxs.select(r'//ul[@id="paper-listing"]//a/@href').extract():
            yield Request(urlparse.urljoin(response.url, href), callback=self.parse_paper)
        next = hxs.select(r'//div[@class="pagination"]/ul/li[@class="next"]/a/@href')
        if len(next):
            yield Request(urlparse.urljoin(response.url, next[0].extract()), callback=self.parse_list)

    def parse_paper(self, response):
        paper = ResearchPaperItem()
        hxs = HtmlXPathSelector(response)
        content = hxs.select(r'//div[@id="content-small"]')
        paper['title'] = self._jextract(content.select(r'.//h1/text()'))
        for attribute in content.select(r'.//div[@class="briefing-attributes"]/p/text()').extract():
            self._parse_attribute(paper, attribute.strip())
        paper['summary'] = [p for p in content.select(r'./div/div/p/text()').extract()]
        paper['download'] = self._jextract(content.select(r'.//div[@id="full-listing-download"]//a/@href'))

        return [paper]

    def _jextract(self, selector):
        return "".join(selector.extract()).strip()

    def _parse_attribute(self, paper, attribute):
        match = re.search(r'Authors:\s+(.*)$', attribute)
        if match:
            paper['authors'] = map(lambda item: item.strip(), match.group(1).split(","))
            return
        match = re.search(r'Topic:\s+(.*)$', attribute)
        if match:
            paper['topics'] = map(lambda item: item.strip(), match.group(1).split(","))
            return
        match = re.search(r'Published (?P<date>.*) \| (?:Standard notes|Research papers|Library notes).(?P<note>.*)', attribute)
        if match:
            date = datetime.strptime(match.group('date'), r'%d %B %Y')
            paper['date'] = {"$date":int(time.mktime(date.timetuple()) * 1000)}
            paper['note'] = match.group('note')
            return


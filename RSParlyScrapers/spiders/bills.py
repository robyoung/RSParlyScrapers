from datetime import datetime
import re
import urlparse
import time

from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider

from RSParlyScrapers.items import BillItem

class BillsSpider(CrawlSpider):
    name = 'bills'
    allowed_domains = ['services.parliament.uk']
    start_urls = ['http://services.parliament.uk/bills/']

    date_pattern = re.compile(r"\d{1,2}\.\d{1,2}\.\d{4}")

    def parse(self, response):
        return self.parse_bill_list(response)

    def parse_bill_list(self, response):
        hxs = HtmlXPathSelector(response)
        for row in hxs.select(r'//div[@id="bill-summary"]//table[@class="bill-list"]//tr'):
            if self._extract_class(row) in ["tr1", "tr2"]:
                for href in row.select(".//a/@href").extract():
                    yield Request(urlparse.urljoin(response.url, href), callback=self.parse_bill)

    def parse_bill(self, response):
        hxs = HtmlXPathSelector(response)
        bill = BillItem()

        bill['name'] = self._jextract(hxs.select("//h1/text()"))
        bill['url'] = response.url
        bill['agents'] = self._parse_agents(hxs.select('//dl[@class="bill-agents"]/*'))
        bill['previous_event'] = self._parse_event(hxs.select('//div[@class="last-event"]//li'))
        bill['next_event'] = self._parse_event(hxs.select('//div[@class="next-event"]//li'))
        bill['summary'] = self._parse_summary(hxs.select('//div[@id="bill-summary"]/*'))

        return [bill]

    def _extract_class(self, row):
        return "".join(row.select("@class").extract())

    def _jextract(self, selector):
        """Extract and join a selector"""
        return "".join(selector.extract()).strip()

    def _clean_key(self, key):
        return re.sub(r"\s+", " ", key.replace(":", "").strip())

    def _parse_agents(self, selector):
        agents = {}
        current_agent = None
        for element in selector:
            if element.extract().startswith("<dt"):
                current_agent = self._clean_key(self._jextract(element.select("./text()")))
            elif element.extract().startswith("<dd"):
                agents[current_agent] = self._jextract(element.select("./text()"))
        return agents

    def _parse_event(self, selector):
        if len(selector):
            date = self.date_pattern.search(selector[0].extract())
            if date:
                # dates represented in mongo extended format, this should be done later in the pipeline.
                date = {"$date":int(time.mktime(datetime.strptime(date.group(0), "%d.%m.%Y").timetuple()) * 1000)}
            return {
                "date": date,
                "description": self._jextract(selector[0].select('.//img/@alt'))
            }

    def _parse_summary(self, selector):
        summary = {}
        current_title = None
        for element in selector:
            if element.extract().startswith("<h2"):
                current_title = self._clean_key(self._jextract(element.select("./text()")))
            elif current_title:
                summary.setdefault(current_title, []).append(element.extract())
        return summary

# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class ZgylbxSpider(scrapy.Spider):
    name = 'zgylbx'
    allowed_domains = ['www.zgylbx.com']
    start_urls = 'https://www.zgylbx.com/index.php?m=content&c=index&a=lists&catid=7'
    source = '中国医疗保险网:%s' % start_urls

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_all_page)

    def parse_all_page(self, response):
        for i in range(1, int(response.css(".dpgpages2-m1 :not(.a1)::text")[-1].get())):
            url = '%s&page=%s&k1=&k2=&k3=&k4=' % (self.start_urls, i)
            yield scrapy.Request(url=url, callback=self.parse_page_item)

    def parse_page_item(self, response):
        news = []
        for new in response.css(".imgtxtList3 .wow.fadeInDown"):
            news.append({
                'title': new.css("h3 a::text").get().strip(),
                'detailurl': response.urljoin(new.css("h3 a::attr(href)").get()),
                'context': new.css("div.ct-jj p::text").get().strip(),
                'time': datetime.strptime(new.css("div.li-li1.time span::text").get(), '%Y-%m-%d'),
                'source': self.source
            })
        return news

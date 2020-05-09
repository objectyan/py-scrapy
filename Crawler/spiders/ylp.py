# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import datetime
from scrapy.selector import Selector

class YlpSpider(scrapy.Spider):
    name = 'ylp'
    allowed_domains = ['www.y-lp.com']
    start_urls = 'http://www.y-lp.com/pages/Trend.aspx'
    post_page_url = 'http://www.y-lp.com/ajaxpro/pages_Trend,App_Web_5btmqbsd.ashx'
    source = '医药经理人/医药脸谱网:%s' % start_urls

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse_all_page)

    def parse_all_page(self, response):
        for i in range(1, int(response.css("div.pager a:not(.on)::text")[-2].get())):
            yield scrapy.Request(url=self.post_page_url,
                                 method='POST',
                                 body=json.dumps({
                                     "page": i,
                                     "cond": []
                                 }),
                                 headers={
                                     'X-AjaxPro-Method': 'GetContent'
                                 },
                                 callback=self.parse_page_item)

    def parse_page_item(self, response):
        news = []
        for new in Selector(text=json.loads(response.body)['value']).css('div.news_item'):
            context = new.css("div.info::text").get()
            if context is not None:
                context = context.strip()
            news.append({
                'title': new.css("div.title a::text").get().strip(),
                'detailurl': response.urljoin(new.css("div.title a::attr(href)").get()),
                'context': context,
                'time': datetime.strptime(new.css("div.property div.date::text").get(), '%Y-%m-%d %H:%M:%S'),
                'source': self.source
            })
        return news

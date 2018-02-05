# -*- coding: utf-8 -*-

import json
import re

import scrapy
from scrapy.http.request import Request
from spider_project.items import SpiderProjectItem

from six.moves.urllib import parse

class List_extractSpider(scrapy.Spider):
    taskid = "list_extract"
    name = taskid
    entry = "/exercise/list_basic/1"

    def start_requests(self):
        prefix = self.settings["WEB_APP_PREFIX"]
        result = parse.urlparse(prefix)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        url = parse.urljoin(base_url, self.entry)
        yield Request(
            url=url,
            callback=self.parse_list_page
        )

    def parse_list_page(self, response):
        for req in self.extract_product(response):
            yield req

    def extract_product(self, response):
        result = parse.urlparse(response.url)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        links = response.xpath("//table//a/@href").extract()
        for url in links:
            url = parse.urljoin(base_url, url)
            yield Request(
                url=url,
                callback=self.parse_product_page
            )

    def parse_product_page(self, response):
        item = SpiderProjectItem()
        item["taskid"] = self.taskid
        data = {}
        title = response.xpath("//div[@class='product-title']/text()").extract()
        price = response.xpath(
            "//div[@class='product-price']/text()"
        ).extract()
        data["title"] = title
        data["price"] = price
        data["sku"] = re.findall("detail/(\d+)", response.url)[0]

        item["data"] = data
        yield item


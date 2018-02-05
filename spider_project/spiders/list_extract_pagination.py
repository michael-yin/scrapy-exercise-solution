# -*- coding: utf-8 -*-

import json
import re

import scrapy
from scrapy.http.request import Request
from spider_project.items import SpiderProjectItem

from six.moves.urllib import parse

class List_extractpaginationSpider(scrapy.Spider):
    taskid = "list_extract_pagination"
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

        for req in self.gene_next_pages(response):
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

    def gene_next_pages(self, response):
        """
        This method will extract all list page from first to the last one

        Actually this method will be called in every list page processing method
        in this spider, scrapy have built in duplicate filter so even you yield
        same url more than onece, the request will only be sent to web server by
        once, which is very good design.
        """
        prefix = self.settings["WEB_APP_PREFIX"]
        result = parse.urlparse(prefix)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        json_txt = "".join(response.xpath("//script[@id='page_data']/text()").extract())
        json_data = json.loads(json_txt)
        total_pages = int(json_data["pages"])
        for i in range(1, total_pages + 1):
            url = parse.urljoin(base_url, "content/list_basic/" + str(i))
            yield Request(
                url=url,
                callback=self.parse_list_page
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


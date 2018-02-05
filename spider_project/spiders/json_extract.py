# -*- coding: utf-8 -*-

import json

import scrapy
from scrapy.http.request import Request
from spider_project.items import SpiderProjectItem

from six.moves.urllib import parse

class Json_extractSpider(scrapy.Spider):
    taskid = "json_extract"
    name = taskid
    entry = "/exercise/detail_json"

    def start_requests(self):
        prefix = self.settings["WEB_APP_PREFIX"]
        result = parse.urlparse(prefix)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        url = parse.urljoin(base_url, self.entry)
        yield Request(
            url=url,
            callback=self.parse_entry_page
        )

    def parse_entry_page(self, response):
        json_txt = "".join(response.xpath("//script[@id='json_data']/text()").extract())
        json_data = json.loads(json_txt)

        item = SpiderProjectItem()
        item["taskid"] = self.taskid
        data = {}
        data["title"] = json_data["title"]
        data["price"] = json_data["price"]
        item["data"] = data
        yield item


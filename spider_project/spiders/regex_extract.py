# -*- coding: utf-8 -*-

import json
import re

import scrapy
from scrapy.http.request import Request
from spider_project.items import SpiderProjectItem

import six
from six.moves.urllib import parse

class Regex_extractSpider(scrapy.Spider):
    taskid = "regex_extract"
    name = taskid
    entry = "/exercise/detail_regex"

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
        result = parse.urlparse(response.url)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        ajax_url = parse.urljoin(base_url, "static/js/content/detail_regex.js")
        yield Request(
            url=ajax_url,
            callback=self.parse_js_file
        )

    def parse_js_file(self, response):
        if isinstance(response.body, six.text_type):
            html = response.body
        else:
            html = response.body.decode(response.encoding)

        json_txt = re.findall("var data =(.+?);", html, re.S)[0]
        json_data = json.loads(json_txt)

        item = SpiderProjectItem()
        item["taskid"] = self.taskid
        data = {}
        data["title"] = json_data["title"]
        data["price"] = json_data["price"]
        item["data"] = data
        yield item


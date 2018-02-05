# -*- coding: utf-8 -*-

import json

import scrapy
from scrapy.http.request import Request
from spider_project.items import SpiderProjectItem

from six.moves.urllib import parse

class Ajax_cookieinfoSpider(scrapy.Spider):
    taskid = "ajax_cookie"
    name = taskid
    entry = "exercise/detail_cookie"

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

        # try to get token from cookie
        ls = response.headers.getlist('Set-Cookie')
        tmp_dic = {}
        for k, v in [i.decode("utf-8").split(";")[0].split("=") for i in ls]:
            tmp_dic[k] = v
        token = tmp_dic["token"]

        ajax_url = parse.urljoin(base_url, "exercise/ajaxdetail_cookie")
        ajax_url = ajax_url + "?token=" + token

        meta = response.meta
        meta["description"] = response.xpath(
            "//section[contains(@class, 'product-info')]/li/text()").extract()

        headers = {
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
            "referer": response.url,
            "X-Requested-With": "XMLHttpRequest",
        }

        yield Request(
            headers=headers,
            meta=meta,
            url=ajax_url,
            callback=self.parse_ajax_page
        )

    def parse_ajax_page(self, response):
        json_data = json.loads(response.body.decode("utf-8"))

        item = SpiderProjectItem()
        item["taskid"] = self.taskid
        data = {}
        data["title"] = json_data["title"]
        data["description"] = response.meta["description"]
        data["price"] = json_data["price"]
        item["data"] = data
        yield item


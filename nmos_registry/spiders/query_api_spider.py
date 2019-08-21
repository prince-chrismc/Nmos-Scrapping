import scrapy
from datetime import datetime
import os
import pathlib
import json
import sys

# datetime object containing current date and time
now = datetime.now()
folder = now.strftime("%d-%m-%Y/%H-%M-%S/")
pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

args = json.loads(sys.argv[-1])
print(args)

class QuerySpider(scrapy.Spider):
    name = "query"

    def start_requests(self):
        urls = [
            'nodes',
            'devices',
            'senders',
            'receivers',
            'sources',
            'flows',
        ]

        for url in urls:
            href = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=update&paging.limit=10000'.format(args["ip"], args["port"], args["api_ver"], url)
            yield scrapy.http.JSONRequest(url=href, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1].split("?")[0]
        filename = 'query-{0}.json'.format(page)
        with open(folder + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

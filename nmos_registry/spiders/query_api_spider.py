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
            'nodes/',
            'devices/',
            'senders/',
            'receivers/',
            'sources/',
            'flows/',
        ]

        href = 'http://{0}:{1}/x-nmos/query/{2}/'.format(args["ip"], args["port"], args["api_ver"])
        for url in urls:
            yield scrapy.http.JSONRequest(url=href+url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = 'query-%s.json' % page
        with open(folder + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

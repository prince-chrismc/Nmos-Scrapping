import scrapy
from datetime import datetime
import os
import pathlib

# datetime object containing current date and time
now = datetime.now()
folder = now.strftime("%d-%m-%Y/%H-%M-%S/")
pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

class QuerySpider(scrapy.Spider):
    name = "query"

    def start_requests(self):
        urls = [
            'http://192.168.3.45/',
            'http://192.168.3.45/x-nmos/query/v1.2/nodes/',
            'http://192.168.3.45/x-nmos/query/v1.2/devices/',
            'http://192.168.3.45/x-nmos/query/v1.2/senders/',
            'http://192.168.3.45/x-nmos/query/v1.2/receivers/',
            'http://192.168.3.45/x-nmos/query/v1.2/sources/',
            'http://192.168.3.45/x-nmos/query/v1.2/flows/',
        ]

        for url in urls:
            yield scrapy.http.JSONRequest(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.json' % page
        with open(folder + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

import scrapy
from datetime import datetime
import os
import pathlib
import json
import sys
import requests

# datetime object containing current date and time
now = datetime.now()
folder = now.strftime("%d-%m-%Y/%H-%M-%S/")
pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

args = json.loads(sys.argv[-1])
print(args)

class QuerySpider(scrapy.Spider):
    name = "query"
    custom_settings = {
        'TELNETCONSOLE_ENABLED': False,
        'LOG_LEVEL': 'WARNING',
    }

    def start_requests(self):
        urls = [
            'nodes',
            'devices',
            'senders',
            'receivers',
            'sources',
            'flows',
        ]


        r = requests.get('http://{0}:{1}/x-nmos/query/{2}/nodes?paging.order=create&paging.limit=10000000000000'.format(args["ip"], args["port"], args["api_ver"]))
        try:
            lim = r.headers['X-Paging-Limit']
        except:
            lim = -1

        print('Paging Limit: {0}'.format(lim))

        for url in urls:
            href = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}'.format(args["ip"], args["port"], args["api_ver"], url, lim)
            yield scrapy.http.JSONRequest(url=href, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1].split("?")[0]
        filename = 'query-{0}'.format(page)
        with open(folder + filename + '.json', 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        try:
            since = response.headers['X-Paging-Since']
            until = response.headers['X-Paging-Until']
            if since != b'0:0' and since != until:
#                print('- Since: {0} // Until: {1}'.format(since, until))
                print('More then paging.limit {0}'.format(page))
                r = requests.get(response.url + '&paging.since='.format(until[1:-1]))
                with open(folder + filename + '-2.json', 'wb') as f:
                    f.write(r.content)
        except:
             pass

    def closed(spider, reason):
        if reason == 'finished':
            for filename in os.listdir(folder):
                handle = open(folder + filename)
                data = json.load(handle)
                print('Resource in {0}: {1}'.format(filename, len(data)))

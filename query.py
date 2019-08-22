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

class QueryScrapper():
    name = "query"
    endpoints = [
        'nodes',
        'devices',
        'senders',
        'receivers',
        'sources',
        'flows',
    ]

    def determine_paging_limit():
        r = requests.get('http://{0}:{1}/x-nmos/query/{2}/nodes?paging.order=create&paging.limit=10000000000000'.format(args["ip"], args["port"], args["api_ver"]))
        try:
            lim = r.headers['X-Paging-Limit']
        except:
            lim = -1

#        print('Paging Limit: {0}'.format(lim))
        return lim

    def start_requests(self):
        lim = QueryScrapper.determine_paging_limit()
        for url in self.endpoints:
            href = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}'.format(args["ip"], args["port"], args["api_ver"], url, lim)

            index = 0
            since = '0:0'
            until = '0:1'

            while True:
                print('GET - ' + href + '&paging.since=' + until)
                r = requests.get(href + '&paging.since=' + until)
#                print(r.headers)
                since = r.headers['X-Paging-Since']
                until = r.headers['X-Paging-Until']
#                print('Since: {0} // Until: {1}'.format(since, until))
                if since == '0:0' or since == until:
                    print('Obtained all ' + url)
                    break

#                print('More then paging.limit of ' + url)
                filename = 'query-' + url
                with open(folder + filename + '-{0}.json'.format(index), 'wb') as f:
                    index += 1
                    f.write(r.content)

    def close(self):
        for filename in os.listdir(folder):
            handle = open(folder + filename)
            data = json.load(handle)
            print('Resource in {0}: {1}'.format(filename, len(data)))

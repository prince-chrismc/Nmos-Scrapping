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

    def save_response(response, index = 0, resource = 'unknown'):
        with open(folder + 'query-' + resource + '-{0}.json'.format(index), 'wb') as f:
            f.write(response.content)

    def start_requests(self):
        lim = QueryScrapper.determine_paging_limit()
        for resource in self.endpoints:
            href = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}'.format(args["ip"], args["port"], args["api_ver"], resource, lim)

            index = 0
            since = '0:0'
            until = '0:0'

            while True:
                link = href
                if index > 0:
                    link += '&paging.since=' + until

                print('\nGET - ' + link)
                r = requests.get(link)
                QueryScrapper.save_response(r, index, resource)
                index += 1

#                print(r.headers)
                since = r.headers['X-Paging-Since']
                until = r.headers['X-Paging-Until']
#                print('Since: {0} // Until: {1}'.format(since, until))
                if since == '0:0' or since == until:
                    print('Obtained all ' + resource)
                    break

                print('More then paging.limit of ' + resource)

    def close(self):
        for filename in os.listdir(folder):
            handle = open(folder + filename)
            data = json.load(handle)
            print('Resource in {0}: {1}'.format(filename, len(data)))

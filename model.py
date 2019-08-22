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

def determine_paging_limit():
    r = requests.get('http://{0}:{1}/x-nmos/query/{2}/nodes?paging.order=create&paging.limit=10000000000000'.format(args["ip"], args["port"], args["api_ver"]))
    try:
        lim = r.headers['X-Paging-Limit']
    except:
        lim = -1

#    print('Paging Limit: {0}'.format(lim))
    return lim

def start_requests():
    lim = determine_paging_limit()
    href_nodes = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}'.format(args["ip"], args["port"], args["api_ver"], 'nodes', lim)
#    print('GET - ' + href_nodes)
    r = requests.get(href_nodes)

    data = json.loads(r.content)
    print('There are {0} nodes'.format(len(data)))
    for node in data:
        parse_node(node['id'])


def parse_node(node_id):
    lim = determine_paging_limit()
    href_associated_devices = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}&node_id={5}'.format(args["ip"], args["port"], args["api_ver"], 'devices', lim, node_id)
#    print('GET - ' + href_associated_devices)
    r = requests.get(href_associated_devices)

    data = json.loads(r.content)
    print('\nNode { ' + node_id + ' } has the following ' + '{0} devices...'.format(len(data)))
    for device in data:
        print('- ' + device['id'])
        href_receivers = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}&device_id={5}'.format(args["ip"], args["port"], args["api_ver"], 'receivers', lim, device['id'])
#        print('GET - ' + href_receivers)
        r = requests.get(href_receivers)
        data = json.loads(r.content)
        for receiver in data:
            print('R   - ' + receiver['id'])

        if len(data) > 0:
            print()

        href_sources = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}&device_id={5}'.format(args["ip"], args["port"], args["api_ver"], 'sources', lim, device['id'])
#        print('\nGET - ' + href_sources)
        r = requests.get(href_sources)
        data = json.loads(r.content)
        for source in data:
            print('S   - ' + source['id'])
            href_flows = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}&source_id={5}'.format(args["ip"], args["port"], args["api_ver"], 'flows', lim, source['id'])
#            print('\nGET - ' + href_flows)
            r = requests.get(href_flows)
            data = json.loads(r.content)
            for flow in data:
                print('F       - ' + flow['id'])
                href_flows = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}&flow_id={5}'.format(args["ip"], args["port"], args["api_ver"], 'senders', lim, flow['id'])
#                print('\nGET - ' + href_flows)
                r = requests.get(href_flows)
                data = json.loads(r.content)
                for sender in data:
                    print('T           - ' + sender['id'])

start_requests()

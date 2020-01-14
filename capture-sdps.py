from datetime import datetime
import os
import pathlib
import json
import sys
import requests
from jsonschema import validate

# datetime object containing current date and time
now = datetime.now()
folder = now.strftime("%d-%m-%Y/%H-%M-%S/")
pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

args = json.loads(sys.argv[-1])
print(args)

schema = {
    "type" : "object",
    "properties" : {
        "ip" : {"type" : "string"},
        "port" : {"type" : "number"},
        "api_ver" : {"type" : "string"},
    },
}

validate(instance=args, schema=schema)

def determine_paging_limit():
    r = requests.get('http://{0}:{1}/x-nmos/query/{2}/senders?paging.order=create&paging.limit=10000000000000'.format(args["ip"], args["port"], args["api_ver"]))
    try:
        lim = r.headers['X-Paging-Limit']
    except:
        lim = -1

    print('Paging Limit: {0}'.format(lim))
    return lim

def start_requests():
    lim = determine_paging_limit()
    href = 'http://{0}:{1}/x-nmos/query/{2}/{3}?paging.order=create&paging.limit={4}'.format(args["ip"], args["port"], args["api_ver"], 'senders', lim)
    print('GET - ' + href)
    r = requests.get(href)

    since = '0:0'
    until = '0:1'

    while True:
       print('GET - ' + href + '&paging.since=' + until)
       r = requests.get(href + '&paging.since=' + until)
#       print(r.headers)
       since = r.headers['X-Paging-Since']
       until = r.headers['X-Paging-Until']
       print('Since: {0} // Until: {1}'.format(since, until))
       if since == '0:0' or since == until:
          print('Obtained all senders')
          break

       print('More then paging.limit of senders')
       data = json.loads(r.content)
       for sender in data:
           if not 'manifest_href' in sender:
              print(sender)
              continue
           if not 'id' in sender:
              print(sender)
              continue
           if sender.get('manifest_href') == None:
              print(sender)
              continue

           fetch_sdp(sender['id'], sender['manifest_href'])

def fetch_sdp(sender_id, sender_manifest_href):
    print('GET - ' + sender_id + ' - ' + sender_manifest_href)
    try:
        r = requests.get(sender_manifest_href)
        if r.status_code == 404:
            raise Exception('obtained a 404')
    except:
        print('SDP file was un-obtainable')
    else:
        filename = sender_id + '.sdp'
        with open(folder + filename, 'wb') as f:
           f.write(r.content)

start_requests()

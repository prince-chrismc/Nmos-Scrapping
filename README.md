# Nmos-Scrapping

Very basic RDS scrapping tool.

run `python3 scrap-query.py '{"ip":"192.168.3.45","port":80,"api_ver":"v1.2"}'` to get a timestamped dump of the RDS.


### Analysis
- Number of active vs inactive senders
```sh
cat 23-08-2019/02-52-36/query-senders-*.json | grep -o \"active\":true | wc -l
cat 23-08-2019/02-52-36/query-senders-*.json | grep -o \"active\":false | wc -l
```

- Number of input only devices
```sh
cat 23-08-2019/04-45-31/query-devices-*.json | grep -o '"senders":\[\]' | wc -l
```

- Number devices comparison
```sh
  686  cat query-devices-*.json | egrep '"id":' -o | wc -l                 # number of devices
  687  cat query-devices-*.json | grep -o '"receivers":\[\]' | wc -l       # number of output only devices
  688  cat query-receivers-*.json | egrep 'device_id":"[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}' -o | sort --unique | wc -l # Number of devices as reported by receivers
```

- Break down of the types of receivers
```sh
python3 model.py '{"ip":"192.168.3.45","port":80,"api_ver":"v1.2"}' > model-dump.txt
cat model-dump.txt | grep 'R' | grep 'video' | wc -l
cat model-dump.txt | grep 'R' | grep 'audio' | wc -l
cat model-dump.txt | grep 'R' | grep 'data' | wc -l
```

```sh
cat 23-08-2019/04-45-31/query-receivers-*.json | grep -o 'urn:x-nmos:format:video' | wc -l
cat 23-08-2019/04-45-31/query-receivers-*.json | grep -o 'urn:x-nmos:format:audio' | wc -l
cat 23-08-2019/04-45-31/query-receivers-*.json | grep -o 'urn:x-nmos:format:data' | wc -l
```

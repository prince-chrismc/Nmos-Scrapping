# Nmos-Scrapping

Very basic RDS scrapping tool.

run `python3 scrap-query.py '{"ip":"192.168.3.45","port":80,"api_ver":"v1.2"}'` to get a timestamped dump of the RDS.


### Analysis
- Number of active vs inactive senders
```sh
cat 23-08-2019/02-52-36/query-senders-0.json | grep -o \"active\":true | wc -l
cat 23-08-2019/02-52-36/query-senders-0.json | grep -o \"active\":false | wc -l
```

- Number of audio receivers
```sh
python3 model.py '{"ip":"192.168.3.45","port":80,"api_ver":"v1.2"}' | grep 'R' | grep -o 'audio' | wc -l
```

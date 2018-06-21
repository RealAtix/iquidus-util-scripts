#!/usr/bin/env python3
import requests
import json
import csv

base_url = "https://blockchain.ignitioncoin.org"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
start = 100 # Start at block #
amount = 100 # Process # blocks
data = []

print('Explorer url: {}\n'.format(base_url))
print('Fetching data...')
for n in range(start, start + amount + 1):
    r = requests.get('{}/api/getblockhash?index={}'.format(base_url, n), headers=headers)
    r = requests.get('{}/api/getblock?hash={}'.format(base_url, r.text), headers=headers)
    entry = []
    entry.append(r.json()['height'])
    entry.append(r.json()['time'])
    entry.append(r.json()['difficulty'])
    entry.append(r.json()['flags'])
    print(entry)
    data.append(entry)

with open('blockdata.csv','w') as f:
    print("Writing blockdata.csv")
    writer = csv.writer(f)
    writer.writerows(data)

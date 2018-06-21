#!/usr/bin/env python3
import requests
import json
import numpy
import datetime

base_url = "https://blockchain.ignitioncoin.org"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
amount = 100
data = []
t_next = None
nPoW = 0
nPoS = 0

nBest = int(requests.get('{}/api/getblockcount'.format(base_url), headers=headers).text)
for n in range(nBest, nBest - amount, -1):
    r = requests.get('{}/api/getblockhash?index={}'.format(base_url, n), headers=headers)
    r = requests.get('{}/api/getblock?hash={}'.format(base_url, r.text), headers=headers)
    if ('proof-of-stake' in r.json()['flags']):
        nPoS += 1
    elif ('proof-of-work' in r.json()['flags']):
        nPoW += 1
    if (t_next == None):
        t_next = r.json()['time']
        continue

    time = t_next - r.json()['time']
    t_next = r.json()['time']
    data.append(time)

block_mean = numpy.round(numpy.mean(data), 4)
block_mean_f = str(datetime.timedelta(seconds=block_mean))
block_std = numpy.round(numpy.std(data), 4)
block_std_f = str(datetime.timedelta(seconds=block_std))
block_min = numpy.round(numpy.min(data), 4)
block_min_f = str(datetime.timedelta(seconds=int(block_min)))
block_max = numpy.round(numpy.max(data), 4)
block_max_f = str(datetime.timedelta(seconds=int(block_max)))
print('Explorer url: {}\n'.format(base_url))
print('Block time over the last {} blocks \nmean: {} or {}\nstd: {} or {}\nmin: {} or {}\nmax: {} or {}'.format(amount, block_mean, block_mean_f, block_std, block_std_f, block_min, block_min_f, block_max, block_max_f))
print('\nBlock type\nPoW: {}\nPoS: {}'.format(nPoW, nPoS))

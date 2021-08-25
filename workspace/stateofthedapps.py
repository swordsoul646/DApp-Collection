import datetime
import json
import time
import urllib.parse

import webDataUtils

webDataUtils.setDebug(False)
webDataUtils.setPath('/blockchain/workspace/result/')
webDataUtils.startTimer(60)

req_data = {
    'limit': 100,
    'offset': 0,
    'order': 'asc',
    'sort': 'rank'
}

url = 'https://api.stateofthedapps.com/dapps'

data = []
while True:
    req_data['offset'] = len(data)
    url_full = url + '?' + urllib.parse.urlencode(req_data)
    # print(url_full)
    o = {}
    while True:
        try:
            time.sleep(0.5)
            html = webDataUtils.getWebData(url_full)
            o = json.loads(html)
            data += o['items']
            break
        except Exception as e:
            print('{0} fail, try again...'.format(url_full))
    print(str(len(data)))
    if len(data) >= o['pager']['totalCount']:
        break
# break

print('')

for i in range(0, len(data)):
    dapp = data[i]
    url_dapp = url + '/' + dapp['slug']
    while True:
        html = webDataUtils.getWebData(url_dapp)
        try:
            time.sleep(0.5)
            o = json.loads(html)
            data[i] = o['item']
            break
        except Exception as e:
            print(str(i) + '\t' + dapp['slug'] + ' retry......')
    print(str(i + 1) + '\t' + dapp['slug'])
# break

webDataUtils.writeJSONFile('stateofthedapps-{0}'.format(str(datetime.date.today()).replace('-', '')), data)

print('\ndone')

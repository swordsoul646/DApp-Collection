import json
import time

import webDataUtils

# Setings
url = 'https://api.etherscan.io/api?'
values = {'module': 'account',
          'action': '',
          'address': '',
          'startblock': 0,
          'endblock': 9999999,
          'page': 1,
          'offset': 1,
          'sort': 'asc',
          'apikey': 'Y889VAHVT94SYRIZRMKHRNNYBPGC36RPJE'
          }

webDataUtils.setDebug(False)
webDataUtils.setPath('/blockchain/workspace/result/201901/')

webDataUtils.startTimer(60 * 5)

con_reverse_list = webDataUtils.readJSONFile('con_reverse_list')

output = {}

for addr in con_reverse_list:
    tmp = {
        'type': '',
        'txn': {}
    }
    values['address'] = addr
    try:
        time.sleep(0.5)
        values['action'] = 'txlistinternal'
        ret = json.loads(webDataUtils.getWebData(url + webDataUtils.encodeParams(values)))
        tmp['txn'] = ret['result'][0]
        if tmp['txn']['type'] == 'create' and tmp['txn']['contractAddress'] == addr:
            tmp['type'] = 'son_contract'
    except Exception as e:
        tmp['type'] = ''
    if len(tmp['type']) == 0:
        try:
            time.sleep(0.5)
            values['action'] = 'txlist'
            ret = json.loads(webDataUtils.getWebData(url + webDataUtils.encodeParams(values)))
            tmp['txn'] = ret['result'][0]
            if tmp['txn']['contractAddress'] == addr:
                tmp['type'] = 'root_contract'
            else:
                tmp['type'] = 'user'
        except Exception as e:
            tmp['type'] = 'user'
    output[addr] = tmp
    print(addr + '\t' + tmp['type'])
# break

webDataUtils.writeJSONFile('con_creation_txn', output)

print('Done!')

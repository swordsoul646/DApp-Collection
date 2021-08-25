import re

import webDataUtils

webDataUtils.setPath('/blockchain/workspace/result/')
webDataUtils.checkFolder('201901')

# get transactions
o_sodapp = webDataUtils.readJSONFile('stateofthedapps-20190129')

webDataUtils.setPath('/blockchain/workspace/result/201901/')

dict_dapp_contracts = {}

print('Generating Table......')
for dapp in o_sodapp:
    slug = dapp['slug']
    if dapp['platform'] != 'Ethereum' or dapp['created'] >= '2019-01-01':
        continue
    tmp = {}
    print(slug)
    if len(dapp['contractsMainnet']) > 0:
        for con in dapp['contractsMainnet']:
            addrs = con.replace(' ', '').split(',')
            for addr in addrs:
                if addr.startswith('0x'):
                    tmp[addr] = 1
    if len(tmp) != 0:
        dict_dapp_contracts[slug] = tmp
# break

print('Cleaning......')
for slug in dict_dapp_contracts:
    tmp = {}
    for addr in dict_dapp_contracts[slug]:
        if len(addr) > 42:
            arr = re.split('[^\d\w]+', addr)
            for snippet in arr:
                if len(snippet) != 0 and snippet not in tmp:
                    tmp[snippet[:42].lower()] = 1
        elif len(addr) == 42:
            tmp[addr.lower()] = 1
    dict_dapp_contracts[slug] = tmp

for slug in dict_dapp_contracts:
    tmp = []
    for addr in dict_dapp_contracts[slug]:
        tmp.append(addr)
    dict_dapp_contracts[slug] = tmp

print('Generating Reverse Table......')
dict_contract_dapps = {}
for slug in dict_dapp_contracts:
    for addr in dict_dapp_contracts[slug]:
        if dict_contract_dapps.get(addr) is None:
            dict_contract_dapps[addr] = [slug]
        else:
            dict_contract_dapps[addr].append(slug)

webDataUtils.writeJSONFile('con_list', dict_dapp_contracts)
webDataUtils.writeJSONFile('con_reverse_list', dict_contract_dapps)

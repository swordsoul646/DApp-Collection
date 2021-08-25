import gc
import json

import webDataUtils

webDataUtils.setDebug(False)
webDataUtils.setPath('/blockchain/workspace/result/201901/')

url = 'https://api.etherscan.io/api?'
# Block 4101695: Aug-01-2017 00:00:46
# Block 4832686: Jan-01-2018 00:00:02
# Block 6065979: Jul-31-2018 23:59:53
# Block 6988614: Dec-31-2018 23:59:42
START_BLOCK = 4832686
END_BLOCK = 6988614
values = {'module': 'account',
          'action': 'txlist',
          'address': '',
          'startblock': START_BLOCK,
          'endblock': END_BLOCK,
          'page': 1,
          'offset': 10000,
          'sort': 'asc',
          'apikey': 'Y889VAHVT94SYRIZRMKHRNNYBPGC36RPJE'
          }

webDataUtils.startTimer(60 * 15)

cct = webDataUtils.readJSONFile('con_creation_txn')

webDataUtils.checkFolder('txns')
webDataUtils.setPath('/blockchain/workspace/result/201901/txns/')

for addr in cct:
    if cct[addr]['type'] == 'user':
        continue
    webDataUtils.checkFolder(addr)
    if webDataUtils.checkFile(addr + '/0'):
        print(addr + ': pass')
        continue
    print(addr)
    txn_list = []
    values['address'] = addr
    values['startblock'] = START_BLOCK
    values['endblock'] = END_BLOCK
    values['page'] = 1
    values['offset'] = 1
    firstBlock = START_BLOCK
    lastBlock = END_BLOCK

    # get firstBlock
    values['sort'] = 'asc'
    while True:
        ret = webDataUtils.getWebData(url + webDataUtils.encodeParams(values))
        if ret != '':
            o = json.loads(ret)
            if o.get('result') is not None and str(type(o['result'])) == "<class 'list'>":
                if len(o['result']) == 0:
                    firstBlock = lastBlock + 1
                else:
                    firstBlock = int(o['result'][0]['blockNumber'])
                break

    # get lastBlock
    values['sort'] = 'desc'
    if firstBlock <= lastBlock:
        web_get_count = 0
        while True:
            ret = webDataUtils.getWebData(url + webDataUtils.encodeParams(values))
            if ret != '':
                o = json.loads(ret)
                if o.get('result') is not None and str(type(o['result'])) == "<class 'list'>":
                    lastBlock = int(o['result'][0]['blockNumber'])
                break
            web_get_count += 1
            if web_get_count == 10:
                webDataUtils.log('Wget {0} fail in 10 times...... set lastBlock to default value {1}'.format(
                    url + webDataUtils.encodeParams(values), lastBlock))
                # lastBlock = END_BLOCK
                break

    # recover parameters
    values['sort'] = 'asc'
    values['offset'] = 10000
    print('\t' + str(firstBlock) + ' - ' + str(lastBlock))
    txn_count = 0
    block_delta = 2000

    write_count = 0
    if firstBlock <= lastBlock:
        for fromblock in range(firstBlock, lastBlock + 1, block_delta):
            values['startblock'] = fromblock
            values['endblock'] = fromblock + block_delta - 1
            if values['endblock'] > lastBlock:
                values['endblock'] = lastBlock
            values['page'] = 0
            while True:
                values['page'] += 1
                o = {}
                while True:
                    ret = webDataUtils.getWebData(url + webDataUtils.encodeParams(values))
                    if ret != '':
                        o = json.loads(ret)
                        if o.get('result') is not None and str(type(o['result'])) == "<class 'list'>":
                            break
                txn_list += o['result']
                txn_count += len(o['result'])
                if len(o['result']) < 10000:
                    break
            print('\t' + str(values['startblock']) + ' - ' + str(values['endblock']) + ': ' + str(txn_count))
            if len(txn_list) > 100000 and (lastBlock - fromblock) >= 100000:
                webDataUtils.writeJSONFile(addr + '/' + str(write_count), txn_list)
                print('\twrite: {0}/{1}.json'.format(addr, write_count))
                write_count += 1
                txn_list = []
                gc.collect()
        print(addr + ': ' + str(txn_count))
        webDataUtils.writeJSONFile(addr + '/' + str(write_count), txn_list)
        del txn_list
    else:
        webDataUtils.writeJSONFile(addr + '/0', txn_list)
    gc.collect()
# break

print('Done!')

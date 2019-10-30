# DApp Collection
 Some programs to get DApp metadata
 
 The dataset is used in ["A First Look at Blockchain-based Decentralized Applications"](https://doi.org/10.1002/spe.2751)

## workspace/stateofthedapps.py
 Get dapps' metadata from stateofthedapps.com

 Output

 * workspace/result/stateofthedapps-xxxxxx.json

## workspace/con_list_generate.py
 Generate contract table from stateofthedapps.com

 Output

 * workspace/result/xxxxxx/con_list.json : dapp to contract
 * workspace/result/xxxxxx/con_reverse_list.json : contract to dapp

## workspace/contract_creation_txn_getter.py
 Get contract creation transactions from etherscan.io

 Output

 * workspace/result/xxxxxx/con_creation_txn.json : contract to transaction

## workspace/get_txns.py
 Get related transactions by contract from etherscan.io

 Output

 * workspace/result/xxxxxx/txns : Some json files that keep transactions. Each contract's related transactions are saved in a directory named the contract.

## workspace/get_internal_txns.py
 Get related internal transactions by contract from etherscan.io

 Output

 * workspace/result/xxxxxx/internal_txns : Some json files that keep internal transactions. Each contract's related internal transactions are saved in a directory named the contract.

## workspace/webDataUtils
 A simple tool

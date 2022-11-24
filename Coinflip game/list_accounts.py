import json
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3
from pathlib import Path


# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545/'))

with open(Path('coinflip_abi.json')) as f:
    contract_abi = json.load(f)

contract_address = "0x1b26088bef6E2AF862D65E5607Bfb7c3b850a22D"

contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

accounts = w3.eth.accounts

print(accounts)

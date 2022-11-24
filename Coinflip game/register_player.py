import os
import json
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545/'))

with open(Path('coinflip_abi.json')) as f:
    contract_abi = json.load(f)

contract_address = os.getenv('CURRENT_CONTRACT_ADDRESS')

contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

accounts = w3.eth.accounts

contract.functions.register().transact({"from": w3.eth.accounts[2], "value": 10000000000000000000, "gasPrice": w3.eth.gas_price,})

print('it ran!')

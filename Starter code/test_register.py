import json
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3
from pathlib import Path


# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545/'))

with open(Path('rps_abi.json')) as f:
    contract_abi = json.load(f)

contract_address = "0x28EC59AD969E744ea6Ed09DFE0a1b2F068a98EC8"

contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

accounts = w3.eth.accounts

address = "0x5160D62e1EB93ceeB7ff635E15bE8589972E93aD"
address2 = "0x26eF4E04ac189970b27314da91993a87C1e6245D"


def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


#receipt = contract.functions.BET_MIN().call()

contract.functions.register().transact({"from": w3.eth.accounts[0], "value": 10000000000000000000, "gasPrice": w3.eth.gas_price,})

print('it ran!')

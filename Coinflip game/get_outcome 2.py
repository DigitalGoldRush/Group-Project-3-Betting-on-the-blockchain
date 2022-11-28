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

address = "0x669Ee7f0BfA6BC3D0F932aB22c107FCC7cB9e288"
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

contract.functions.getOutcome().transact({"from": w3.eth.accounts[0], "gasPrice": w3.eth.gas_price,})


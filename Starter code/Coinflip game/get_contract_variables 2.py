#0x669Ee7f0BfA6BC3D0F932aB22c107FCC7cB9e288

import os
import json
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
os.chdir('/Users/michaeldionne/Documents/GitHub/Group Projects/Group Project # 3_Rock_Paper_scissors/Starter code/')


load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545/'))

def load_contract():

    with open(Path('coinflip_abi.json')) as f:
        contract_abi = json.load(f)

    contract_address = os.getenv('CURRENT_CONTRACT_ADDRESS')

    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi,
    )
    return contract 

contract = load_contract()


bet_min = contract.functions.BET_MIN().call()
bet_max = contract.functions.BET_MAX().call()





contract_balance = contract.functions.getContractBalance().call()
initial_bet = contract.functions.initialBet().call()
house_played = contract.functions.housePlayed().call()
player_played = contract.functions.playerPlayed().call()
player_choice = contract.functions.playerChoice().call()
random_number = contract.functions.randomNum().call()
outcome = contract.functions.outcome().call()
paid = contract.functions.paid().call()



print('------------------------------')

print(f'minimum bet: {bet_min}')
print(f'maximum bet: {bet_max}')
print(f'initial bet: {initial_bet}')
print(f'contract balance: {contract_balance}')
print(f'house played status: {house_played}')
print(f'player played status: {player_played}')
print(f'player choice: {player_choice}')
print(f'random number: {random_number}')
print(f'outcome : {outcome}')
print(f'winner was paid: {paid}')


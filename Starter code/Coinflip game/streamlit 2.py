import os
import json
import streamlit as st
from PIL import Image
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
os.chdir('/Users/michaeldionne/Documents/GitHub/Group Projects/Group Project # 3_Rock_Paper_scissors/Starter code/')

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545/'))

# Cache the contract on load
@st.cache(allow_output_mutation=True)


# Define the load_contract function
def load_contract():

    with open(Path('coinflip_abi.json')) as f:
        contract_abi = json.load(f)

    contract_address = "0xF2F94a893698f86A871834E58768E82609707671"
    #contract_address = os.getenv('CURRENT_CONTRACT_ADDRESS')

    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi,
    )
    return contract 

# Load the contract
contract = load_contract()


# create the coinflip game in streamlit
st.title('Coinflip')
st.write('Choose heads or tails. If you win, you get double your bet. If you lose, you lose your bet. Good luck!')

'''
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")
'''


def get_contract_variables():
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
    return bet_min, bet_max, contract_balance, initial_bet, house_played, player_played, player_choice, random_number, outcome, paid


contract_variables = get_contract_variables()

def reset_contract():
    contract.functions.reset_contract().transact({"from": w3.eth.accounts[1], "gasPrice": w3.eth.gas_price,})

def register_player(player):
    contract.functions.register().transact({"from": w3.eth.accounts[player], "value": 10000000000000000000, "gasPrice": w3.eth.gas_price,})

def player_choice(player, choice):
    contract.functions.playerChooses(choice).transact({"from": w3.eth.accounts[player], "gasPrice" : w3.eth.gas_price,})

def get_outcome(player):
    contract.functions.getOutcome().transact({"from": w3.eth.accounts[player], "gasPrice": w3.eth.gas_price,})

player = 5
house = 6

st.write(get_contract_variables())

register_player(house)
register_player(player)

player_choice(player, 1)

get_outcome(player)

'''
st.write(get_contract_variables())



register_player(house)
register_player(player)

st.write('Please select your bet amount in ether.')
st.write('The minimum bet is 1 and the maximum bet is 100')
bet_amount = st.number_input('Bet Amount', value=0, step=0.1)

st.write('Please select heads or tails.')
choice = st.selectbox('Heads or Tails', ('Heads', 'Tails'))
bet_choice = st.selectbox('Bet Choice', options=['Heads', 'Tails'])

player_choice(player, 1)
get_outcome(player)


st.write(get_contract_variables())



bet_min = contract.functions.BET_MIN().call()
bet_max = contract.functions.BET_MAX().call()


if bet_amount < bet_min:
    st.write('Bet amount is too low. Please bet at least 1 ether.')
elif bet_amount > bet_max:
    st.write('Bet amount is too high. Please bet at most 100 ether.')
else:
    if bet_choice == 'Heads':
        bet_choice = 0
    else:bet_choice = 1
    contract.functions.initialBet(bet_choice).transact({"from": w3.eth.accounts[0], "gasPrice": w3.eth.gas_price, "value": w3.toWei(bet_amount, "ether")})  
    st.write('Bet placed. Please wait for the result.')
    st.write('The result is: ', contract.functions.result().call())
    st.write('The winning side is: ', contract.functions.winningSide().call())
    st.write('The winning amount is: ', contract.functions.winningAmount().call())
    st.write('The losing amount is: ', contract.functions.losingAmount().call())
    st.write('The contract balance is: ', contract.functions.getContractBalance().call())
    
reset_contract()

st.write(get_contract_variables())





'''



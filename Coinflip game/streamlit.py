import os
import json
import streamlit as st
from PIL import Image
from web3 import Web3
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from streamlit_lottie import st_lottie  
import requests

# os.chdir('/Users/michaeldionne/Documents/GitHub/Group Projects/Group_Project_3_Coinflip_BlackJack/Coinflip game/')

load_dotenv('.env')

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545/'))

# Cache the contract on load
@st.cache(allow_output_mutation=True)

# Define the load_contract function
def load_contract():

    with open(Path('coinflip_abi.json')) as f:
        contract_abi = json.load(f)
    
    contract_address = os.getenv('CURRENT_CONTRACT_ADDRESS')

    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi,
    )
    return contract 

# Load the contract
contract = load_contract()


#create the coinflip game in streamlit
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
       return None
    return r.json()

lottie_animation_1 = "https://assets1.lottiefiles.com/packages/lf20_1l9gpfir.json"
lottie_anime_json_1 = load_lottie_url(lottie_animation_1)

st.title('Coin Flip! ✨ Choose Heads or Tails')
st_lottie(lottie_anime_json_1, key = "magic", width=300, height=250)  


# To select an account from a connected wallet
#st.write("Choose an account to get started")
#accounts = w3.eth.accounts
#address = st.selectbox("Select Account", options=accounts)
#st.markdown("---")
# def get_contract_variables():
#     bet_min = contract.functions.BET_MIN().call()
#     bet_max = contract.functions.BET_MAX().call()
#     contract_balance = contract.functions.getContractBalance().call()
#     initial_bet = contract.functions.initialBet().call()
#     house_played = contract.functions.housePlayed().call()
#     player_played = contract.functions.playerPlayed().call()
#     player_choice = contract.functions.playerChoice().call()
#     random_number = contract.functions.randomNum().call()
#     outcome = contract.functions.outcome().call()
#     paid = contract.functions.paid().call()
#     return bet_min, bet_max, contract_balance, initial_bet, house_played, player_played, player_choice, random_number, outcome, paid
def reset_contract():
    # contract.functions.reset_contract().transact({"from": w3.eth.accounts[1], "gasPrice": w3.eth.gas_price,})
    contract.functions.reset_contract().transact({"from": w3.eth.accounts[player], "gasPrice": w3.eth.gas_price,})

# def register_player(player):
#     contract.functions.register().transact({"from": w3.eth.accounts[player], "value": 10000000000000000000, "gasPrice": w3.eth.gas_price,})

def register_player(player, bet_amount):
    contract.functions.register().transact({"from": w3.eth.accounts[player], "value": bet_amount, "gasPrice": w3.eth.gas_price,})

def set_player_choice(player, choice):
    contract.functions.playerChooses(choice).transact({"from": w3.eth.accounts[player], "gasPrice" : w3.eth.gas_price,})

def get_outcome(player):
    contract.functions.getOutcome().transact({"from": w3.eth.accounts[player], "gasPrice": w3.eth.gas_price,})

# Address/Index # on Ganache
player = 0
house = 2

#Bet Amount
bet_min = contract.functions.BET_MIN().call()
bet_max = contract.functions.BET_MAX().call()

# st.write('The minimum bet is 1 wei and the maximum bet is 10 ETH')
st.write(f'The minimum bet is {bet_min} wei and the maximum bet is {bet_max/10**18} ETH')
# initial_bet = st.number_input('Bet Amount', value=0, step=10)
initial_bet_eth = st.number_input('Bet Amount', value=0, step=1)
initial_bet_wei = initial_bet_eth * (10**18)

# if initial_bet < bet_min:
if initial_bet_wei < bet_min:
    st.write('Bet amount is too low. Please select a higher bet amount.')
# elif initial_bet_wei > bet_max:
elif initial_bet_wei > bet_max:
    st.write('Bet amount is too high. Please select a lower bet amount.')
else:
    # st.write('You have selected a bet amount of', initial_bet)
    st.write('You have selected a bet amount of', initial_bet_eth)

# Register the player
st.write("Submit Your Bet")
if st.button("Register"):
    register_player(house, initial_bet_wei)
    register_player(player, initial_bet_wei)
    st.write("You have registered!")


# Initial bet
# initial_bet = contract.functions.initialBet().call()

# Player choice
# st.write('Please select heads or tails.')


# resultHead=st.button("Heads")
# if resultHead:
#     # resultHead = 
#     set_player_choice(player, 1)
#     player_choice=1
#     st.write('You have selected heads.')

# resultTail=st.button("Tails")
# if resultTail:
#     # resultTail = 
#     set_player_choice(player, 2)
#     player_choice=2
#     st.write('You have selected tails.')

choices={'Heads': 1, 'Tails': 2}
result=st.selectbox('Please select heads or tails.', ['Heads', 'Tails'])
player_choice=choices[result]
if st.button('Choose'): 
    set_player_choice(player, player_choice)
    # player_choice=2
    # st.write('You have selected tails.')    
    st.write(f'You have selected {result}.')    

if st.button('Get outcome'): 
    get_outcome(player)
    outcome = contract.functions.outcome().call()
    st.write('The outcome is', outcome)
    if player_choice == outcome:
        st.write('You win!')
    else:
        st.write('You lose!')
    reset_contract()

# check = st.checkbox("Ready to flip?")
# if check :
#     st.write('Good Luck!')

#     #placed in this logic to slow execution in streamlit
#     flip_result = st.button('Coin Flip!')
#     # outcome = contract.functions.outcome().call()
#     outcome=get_outcome(player)
#     # get_outcome()

#     # Player choice
#     # player_choice = contract.functions.playerChoice().call()

#     if st.button('Show Result'): 
#         st.write('The outcome is', outcome)
#         if player_choice == outcome:
#             st.write('You win!')
#         else:
#             st.write('You lose!')
            
#     reset_contract()


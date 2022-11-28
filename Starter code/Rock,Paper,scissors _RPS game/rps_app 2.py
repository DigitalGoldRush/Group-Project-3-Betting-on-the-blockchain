import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3
load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    
    with open(Path('./Contracts/Compiled/rockpaperscissors_ABI.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()

st.title("Rock, Paper, Scissors")

if st.button('Play Game'):
    st.write('Hello dear patron, would you like to play a game?')

else:
    st.write('Goodbye')

    
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register New Artwork
################################################################################
option = st.selectbox('Pick a start gesture', ('Rock', 'Paper', 'Scissors'))
                
st.write(option)


################################################################################
# get balance
################################################################################


def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


################################################################################
## send_transaction
################################################################################

def send_transaction(w3, account, to, ether):
    """Send an authorized transaction to the Ganache blockchain."""
    # Set medium gas price strategy
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    # Convert eth amount to Wei
      
    wei_value = w3.toWei(ether, "ether")

    # Calculate gas estimate
    gasEstimate = w3.eth.estimateGas({"to": to, "from": account.address, "value": wei_value})

    # Construct a raw transaction
    raw_tx = {
        "to": to,
        "from": account.address,
        "value": wei_value,
        "gas": gasEstimate,
        "gasPrice": 0,
        "nonce": w3.eth.getTransactionCount(account.address)
    }

    # Sign the raw transaction with ethereum account
    signed_tx = account.signTransaction(raw_tx)

    # Send the signed transactions
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

st.title("Send Ether")

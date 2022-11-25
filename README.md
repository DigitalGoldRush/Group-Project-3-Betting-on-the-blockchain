# Group Project #3: Betting on the Blockchain

[![Gambling Image](https://github.com/DigitalGoldRush/Group-Project-3-Betting-on-the-blockchain/blob/main/media/gambling%20image.jpeg)](https://github.com/DigitalGoldRush/Group-Project-3-Betting-on-the-blockchain/blob/main/media/gambling%20image.jpeg)


## 1. Building smart contracts that run games of chance

### 1.1. The Coin Flip

- ### Coin flip is a simple game of chance with only two outcomes, heads or tails. The contract will return double the user's bet if they win and return nothing if they lose

### 1.2. Black Jack

- ### Black Jack is a game of chance where the user bets on the outcome of a game of Black Jack

- ### The user can bet on the dealer or the player winning. The contract will return the user's bet if they win and return nothing if they lose

### 2. Building a web app (Streamlit) that allows users to interact with the smart contracts

## Summary of Findings

- ### [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/digitalgoldrush/project-2-emotional-recognition/main/Emotion_recognition.ipynb)

---

## Technology Used

[![Python](https://img.shields.io/badge/Python-3.9.12-blue)](https://www.python.org/downloads/release/python-3912/)

[![Solidity](https://img.shields.io/badge/Solidity-0.8.9-blue)](https://docs.soliditylang.org/en/v0.8.9/)

[![Streamlit](https://img.shields.io/badge/Streamlit-0.88.0-blue)](https://docs.streamlit.io/en/stable/)

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DigitalGoldRush?tab=repositories)

---

## Troubleshooting

- ### A common problem encountered is a transaction revert error on the streamlit app.  This is due to some component of the smart contract (that Streamlit interfaces with) is not fulfilled. In that case the user should interact directly with the deployed smart contract on Remix

- ### Here is the transaction revert error



- ### Here are the instructions to clear the error

- 1. #### The state function buttons (orange) need to be pressed in the order of the smart contract format

- 2. #### The error is from the player choosing a coin side to flip and did not press the "choose" button on streamlit. By skipping ahead to the "get outcome" button it skipped the state function "playerChoice" on the smart contract causing the error

- 3. #### To resolve this error, the player must go to the deployed contract on Remix

- 4. #### The "playerChoice" button with the choice ( heads = 1, tails =2) needs to be entered

- 5. #### Then the "getOutcome" button needs to be depressed. This is the "coinflip" portion

- 6. ####  Finally, the "reset_contract" button can be pressed to end the current contract and start a new instance. The player can go back to streamlit and refresh the app & begin a new game

---

## Contributors

[![Python](https://img.shields.io/badge/Michael_Dionne-LinkedIn-blue)](https://www.linkedin.com/in/michael-dionne-b2a1b61b/)

[![Python](https://img.shields.io/badge/David_Lampach-LinkedIn-blue)](https://www.linkedin.com/in/david-lampach-1b21133a/)

---

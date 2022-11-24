pragma solidity ^0.8.17;

import "@openzeppelin/contracts/utils/Strings.sol";

contract BlackJack {

    bool internal locked;
    uint public gameInProgress          = 0;
    uint constant public BET_MIN        = 1 wei;    // The minimum bet
    uint constant public BET_MAX        = 10 ether;
    uint public houseBalance            = 0;
    uint public playerBalance           = 0;
    uint public betAmount               = 0;
    uint randomNum                      = 0;
    uint suit                           = 0;
    uint rank                           = 0;
    uint[2][16] public playersCards;
    uint[2][16] public dealersCards;
    uint[2][4] public dealtCards;
    uint public playerCardCount         = 0;
    uint public dealerCardCount         = 0;
    uint public playerBusted            = 0;
    uint public dealerBusted            = 0;
    uint[2][2] public playerHandValue;
    uint[2][2] public dealerHandValue;
    uint public finalPlayerCount        = 0;
    uint public finalDealerCount        = 0;
    uint public playerStands            = 0;
    uint public dealerStands            = 0;


    string ranNumAsString = "";
    string slicedString = "";
    uint ranNumStringLength;
    uint nonce = 0;
            
    // Players' addresses

    address  playerWallet = address(0x0);
    address  houseWallet = address(0x0);


    function getSlice(uint256 begin, uint256 end, string memory text) internal pure returns (string memory) {
        bytes memory a = new bytes(end-begin+1);
        for(uint i=0;i<=end-begin;i++){
            a[i] = bytes(text)[i+begin-1];
        }
        return string(a);    
    }

    
    function stringToUint(string memory s) internal pure returns (uint) {
        bytes memory b = bytes(s);
        uint result = 0;
        for (uint256 i = 0; i < b.length; i++) {
            uint256 c = uint256(uint8(b[i]));
            if (c >= 48 && c <= 57) {
                result = result * 10 + (c - 48);
            }
        }
        return result;
    }

    // Global mutex modifier

    modifier mutex() { //To prevent reentrancy attacks

        require(!locked, "Reentrancy not allowed");
        locked = true;
        _;
        locked = false;

    }


    function getRandom() internal returns(uint) {
        // increase nonce
        nonce++; 
        randomNum =  uint(keccak256(abi.encodePacked((block.number+(nonce*3)), msg.sender, nonce))) % 1157920892373161954235709850086879078532699846656405640394575840079131296399;
        nonce++;
        return randomNum;
    }
 
    // Player registration function

    modifier validPlayer(uint house_or_player) {

        require(houseWallet == address(0x0) || playerWallet == address(0x0) || msg.sender == houseWallet || msg.sender == playerWallet, "Registration address is not valid");
        require(house_or_player == 0 || house_or_player == 1, "Player must be house(0) or player(1)");
        _;

    }
    
    function fundContract(uint house_or_player) public payable validPlayer(house_or_player) {
        
            
        if (house_or_player == 0) {
            
            require((msg.sender == houseWallet || houseWallet == address(0x0)) && msg.sender != playerWallet, "Sender address must be houseWallet");
            houseWallet = msg.sender;
            houseBalance = houseBalance + msg.value;
        }

        if (house_or_player == 1) {

            require((msg.sender == playerWallet || playerWallet == address(0x0)) && msg.sender != houseWallet, "Sender address must be playerWallet");
            playerWallet  = msg.sender;
            playerBalance = playerBalance + msg.value;               
        }
    }

    // Player Withdrawal Function

    modifier canPlayerWithdraw(uint amount) {

        require(playerBalance > 0, "Player has no balance to withdraw");
        require(msg.sender == playerWallet, "Only player can use this function withdraw");
        require(amount <= playerBalance, "You are requesting more than the player wallet contains");
        _;
    }

    modifier isPlayer() {

        require(msg.sender == playerWallet);
        _;

    }
    
    function playerWithdraw(uint amount) public payable canPlayerWithdraw(amount) mutex() {

        playerBalance = playerBalance - amount;
        payable(playerWallet).transfer(amount);

    }

    // Player place bet function

    modifier validBet(uint _betAmount) {
   
        require(msg.value >= BET_MIN && msg.value <= BET_MAX);
        require(betAmount <= playerBalance, "Bet amount is more than game balance");
        require(msg.sender == playerWallet, "Only player can place bet");
        _;

    }

    function placeBet(uint _betAmount) public payable validBet(betAmount) mutex() {

        playerBalance = playerBalance - _betAmount;
        betAmount = _betAmount;

    }

    function getCards(uint numCards) internal {
        
        uint i = 1;

        while (i <= numCards) {

            uint start = 3;
            uint end = 4;
            rank = 0;
            suit = 0;
            
            randomNum = getRandom();
            ranNumAsString = Strings.toString(randomNum);
            slicedString = getSlice(start, end, ranNumAsString);
            randomNum = stringToUint(slicedString);
            ranNumStringLength = bytes(ranNumAsString).length;

            while (randomNum < 1 || randomNum > 13) {

                start = start + 2;
                end = end + 2;
                slicedString = getSlice(start, end, ranNumAsString);
                randomNum = stringToUint(slicedString);

                if (start > (ranNumStringLength - 3)) {
            
                    start = 3;
                    end = 4;
                    randomNum = getRandom();
                    ranNumAsString = Strings.toString(randomNum);
                    slicedString = getSlice(start, end, ranNumAsString);
                    randomNum = stringToUint(slicedString);
                    ranNumStringLength = bytes(ranNumAsString).length;
            
                }
            }

            rank = randomNum;
            start = start + 2;
            end = end + 2;
            slicedString = getSlice(start, end, ranNumAsString);
            randomNum = stringToUint(slicedString);


            while (randomNum < 1 || randomNum > 4) {

                start = start + 1;
                end = start;
                slicedString = getSlice(start, end, ranNumAsString);
                randomNum = stringToUint(slicedString);

            }
        
            suit = randomNum;  

            dealtCards[i][0] = rank;
            dealtCards[i][1] = suit;
            i = i + 1;

        }
    }       

    function numCardsInArray (uint[2][16] memory array) internal pure returns(uint) {

        uint i = 0;
        uint count = 0;
           
        while (i < 16) {
            if (array[i][0] != 0) {
                count = count + 1;                           
            }
            i = i + 1;
        }

        return count;
        
    } 



    function pushToPlayer(uint _rank, uint _suit, uint index) internal {

        playersCards[index][0] = _rank;
        playersCards[index][1] = _suit;
        playerCardCount = numCardsInArray(playersCards);

    }


    function pushToDealer(uint _rank, uint _suit, uint index) internal {

        dealersCards[index][0] = _rank;
        dealersCards[index][1] = _suit;
        dealerCardCount = numCardsInArray(dealersCards);

    }


    function deal() public mutex {
        
        //Reset the state variables for new hand
        gameInProgress = 1;
        playerStands = 0;
        playerBusted = 0;
        dealerBusted = 0;
        playerStands = 0;
        dealerStands = 0;
        finalDealerCount = 0;
        finalPlayerCount = 0;
        playerHandValue[1][0] = 0;
        playerHandValue[1][1] = 0;

        //Everything in this FOR statement resets all the player and dealer cards to 0
        for (uint256 i = 1; i < 16; i++) {  
            
            playersCards[i][0] = 0;
            playersCards[i][1] = 0;
            dealersCards[i][0] = 0;
            dealersCards[i][1] = 0;

            if (i < 4) {

                dealtCards[i][0] = 0;
                dealtCards[i][1] = 0;

            }

        }



        getCards(3);   //Only first deal gets 3 cards  --  2 for player and 1 (up card) for dealer
        dealtCards = replaceDuplicates(dealtCards);  //Scans the frist 3 dealt cards for duplicates and redraws cards if any two cards are exactly the same (rank and suit).
        pushToPlayer(dealtCards[1][0], dealtCards[1][1], 1);
        pushToDealer(dealtCards[2][0], dealtCards[2][1], 1);
        pushToPlayer(dealtCards[3][0], dealtCards[3][1], 2);
        sumPlayersCards();
        sumDealersCards();
        evaluateDealerHand();  
        evaluatePlayerHand();  

        if (playerHandValue[1][1] == 21) {   // Evaluates if player is dealt blackjack.  If TRUE, game is ended.

            playerHasBlackJack();
        }
        

    }

    modifier _gameInProgress() {
        require(gameInProgress == 1, "Game must be in progress");
        _;
    }

    modifier _playerBusted() {
        require(playerBusted == 0, "You've already busted");
        _;
    }

    //Function to draw one card for the player.  Evaluates the new hand.
    function hitPlayer() public _gameInProgress() _playerBusted() didPlayerStand() {
        
        uint index = numCardsInArray(playersCards);
        getCards(1);
        
        for (uint256 i = 1; i <= index; i++) {
            while ((playersCards[i][0] == dealtCards[1][0]) || (dealersCards[i][0] == dealtCards[1][0])) {
	            if ((playersCards[i][1] == dealtCards[1][1]) || (dealersCards[i][1] == dealtCards[1][1])) {
                    getCards(1);
                }
            }
        }    
    
        pushToPlayer(dealtCards[1][0], dealtCards[1][1], (index + 1));
        sumPlayersCards();
        evaluatePlayerHand();

    }

    //Function to draw one card for the dealer.  Evaluates the new hand.
    function hitDealer() public {
        
        uint index = numCardsInArray(dealersCards);
        getCards(1);
    
        for (uint256 i = 1; i <= index; i++) {
            while ((playersCards[i][0] == dealtCards[1][0]) || (dealersCards[i][0] == dealtCards[1][0])) {
	            if ((playersCards[i][1] == dealtCards[1][1]) || (dealersCards[i][1] == dealtCards[1][1])) {
                    getCards(1);
                }
            }
        }    
    
        pushToDealer(dealtCards[1][0], dealtCards[1][1], (index + 1));
        sumDealersCards();
        evaluateDealerHand();

    }  

    //Counts the players hand value.  Creates [i][0] where aces are 1 and [i][1] where aces are 11.
    function sumPlayersCards() internal {

        uint result = 0;
        uint aceAlready = 0;

        playerCardCount = numCardsInArray(playersCards);

        for (uint256 i = 1; i <= playerCardCount; i++) {

            if (playersCards[i][0] > 9) {
                result = result + 10;
            }
            if (playersCards[i][0] < 10) { 
                result = result + playersCards[i][0];
            }
            if (playersCards[i][0] == 1) {
                aceAlready = 1;           
            }
        }

        playerHandValue[1][0] = result;
        playerHandValue[1][1] = result;
        
        if (aceAlready == 1) {
            
            playerHandValue[1][1] = playerHandValue[1][1] + 10;
        }
    }

    //Counts the dealers hand value.  Creates [i][0] where aces are 1 and [i][1] where aces are 11.
    function sumDealersCards() internal {

        uint result = 0;
        uint aceAlready = 0;

        dealerCardCount = numCardsInArray(dealersCards);

        for (uint256 i = 1; i <= dealerCardCount; i++) {

            if (dealersCards[i][0] > 9) {
                result = result + 10;
            }
            if (dealersCards[i][0] < 10) { 
                result = result + dealersCards[i][0];
            }
            if (dealersCards[i][0] == 1) {
                aceAlready = 1;           
            }
        }

        dealerHandValue[1][0] = result;
        dealerHandValue[1][1] = result;
        
        if (aceAlready == 1) {
            
            dealerHandValue[1][1] = dealerHandValue[1][1] + 10;
        }
    }

    function evaluatePlayerHand() internal {

        if ((playerHandValue[1][0] > 21) && (playerHandValue[1][1] > 21)) {
            playerBusted = 1;
            gameInProgress = 0;
            if (playerHandValue[1][0] <= playerHandValue[1][1]) {
                finalPlayerCount = playerHandValue[1][0];
            }
            if (playerHandValue[1][0] > playerHandValue[1][1]) {
                finalPlayerCount = playerHandValue[1][1];
            }
        }
        if ((playerHandValue[1][0] <= 21) && (playerHandValue[1][1] > 21)) {
            finalPlayerCount = playerHandValue[1][0];
        }
        if ((playerHandValue[1][0] > 21) && (playerHandValue[1][1] <= 21)) {
            finalPlayerCount = playerHandValue[1][1];
        }
        if ((playerHandValue[1][0] <= 21) && (playerHandValue[1][1] <= 21)) {
            if (playerHandValue[1][0] > playerHandValue[1][1]) {
                 finalPlayerCount = playerHandValue[1][0];
            }
            if (playerHandValue[1][0] <= playerHandValue[1][1]) {
                finalPlayerCount = playerHandValue[1][1];
            }
        }
    }

    function evaluateDealerHand() internal {

        if ((dealerHandValue[1][0] > 21) && (dealerHandValue[1][1] > 21)) {
            dealerBusted = 1;
            gameInProgress = 0;
            if (dealerHandValue[1][0] <= dealerHandValue[1][1]) {
                finalDealerCount = dealerHandValue[1][0];
            }
            if (dealerHandValue[1][0] > dealerHandValue[1][1]) {
                finalDealerCount = dealerHandValue[1][1];
            }
        }
        if ((dealerHandValue[1][0] <= 21) && (dealerHandValue[1][1] > 21)) {
            finalDealerCount = dealerHandValue[1][0];
        }
        if ((dealerHandValue[1][0] > 21) && (playerHandValue[1][1] <= 21)) {
            finalDealerCount = dealerHandValue[1][1];
        }
        if ((dealerHandValue[1][0] <= 21) && (dealerHandValue[1][1] <= 21)) {
            if (dealerHandValue[1][0] > dealerHandValue[1][1]) {
                 finalDealerCount = dealerHandValue[1][0];
            }
            if (dealerHandValue[1][0] <= dealerHandValue[1][1]) {
                finalDealerCount = dealerHandValue[1][1];
            }
        }
    }

    modifier didPlayerStand() {

        require(playerStands == 0, "Player has already stood");
        _;
    }

    function playerStand() public didPlayerStand() {

        playerStands = 1;
        evaluatePlayerHand();

    }


    modifier didDealerStand() {

        require(dealerStands == 0, "Dealer has already stood");
        _;
    }

    function dealerStand() public didDealerStand() {

        dealerStands = 1;
        evaluateDealerHand();
        gameInProgress = 0;

    }
    function replaceDuplicates(uint[2][4] memory array) public returns (uint[2][4] memory) {


        while ((array[1][0] == array[2][0]) && (array[1][1] == array[2][1])) {

            getCards(1);
            array[1][0] = dealtCards[2][0];
            array[2][1] = dealtCards[1][1];
                
        }
            
        while ((array[2][0] == array[3][0]) && (array[2][1] == array[3][1])) {

            getCards(1);
            array[3][0] = dealtCards[1][0];
            array[3][1] = dealtCards[1][1];
                           
        }

        return array;

    }

    function playerHasBlackJack() internal {

        gameInProgress = 0;
        
    }

}
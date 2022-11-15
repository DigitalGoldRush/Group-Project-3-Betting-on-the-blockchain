pragma solidity ^0.5.1;

contract CoinFlip {

    uint constant public BET_MIN        = 1 wei;    // The minimum bet
    uint constant public BET_MAX        = 10 ether;
    uint public initialBet;                            // Bet of first player
    uint public outcome;
    uint public randomNum;
    uint public housePlayed = 0;
    uint public playerPlayed = 0;
    uint public playerChoice = 0;
    uint public paid         = 0;


    // Players' addresses
    address payable playerA;
    address payable HouseWallet; // = 0x10b21F7DC7d6BDB16660D827442c7edb3d2523eA; //


    

    /**************************************************************************/
    /*************************** Player Registration **************************/
    /**************************************************************************/


    modifier validBet() {
        require(msg.value >= BET_MIN);
        require(msg.value <= BET_MAX);
        require(initialBet == 0 || msg.value >= initialBet);
        _;
    }

    modifier notAlreadyRegistered() {
        require(msg.sender != playerA);
        
        _;
    }


    function register() public payable validBet notAlreadyRegistered {
        
        if (HouseWallet == address(0x0)) {
            HouseWallet = msg.sender;
            housePlayed = 1;

        }

        else if ( playerA == address(0x0) && HouseWallet != address(0x0) ) {
            playerA    = msg.sender;
            initialBet = msg.value;
            playerPlayed = 1;
      
        }

        
        
    }

    /**************************************************************************/
    /****************************** RESULT PHASE ******************************/
    /**************************************************************************/
    
    
    modifier is_caller_player() {
        
        require(msg.sender == playerA);
        _;
    }

    modifier is_legal_play(uint choice) {
        
        require(choice > 0);
        require(choice < 3);
        _;
    }

        modifier player_never_played {
        
        require(playerChoice < 1);
        _;
    }

    function playerChooses(uint choice) public player_never_played is_caller_player is_legal_play(choice) {

        playerChoice = choice;

    }

    modifier has_player_played {
        
        require(playerChoice > 0);
        _;
    }

    function getOutcome() public has_player_played returns (uint) {
    
        
        randomNum = uint(blockhash(block.number-1)) % 999999;
        

        if (randomNum % 2 == 0) {
            
            outcome = 2;
            if (playerChoice == 2) {

                paid = 1;            
                playerA.transfer(address(this).balance);
                reset();
            
            }

        }

        if (randomNum % 2 == 1) {

            outcome = 1;
            if (playerChoice == 1) {

                paid = 1;
                //reset();  // Reset game before paying to avoid reentrancy attacks
                playerA.transfer(address(this).balance);
                reset();
            
            }

        }
            
        if (paid == 0) {

            
            //reset();  // Reset game before paying to avoid reentrancy attacks
            HouseWallet.transfer(address(this).balance);
            reset();
           

        }
        
    }
    
    // Reset the game.

    function reset() private {
        
        initialBet      = 0;
        playerA         = address(0x0);
        HouseWallet     = address(0x0);
        housePlayed     = 0;
        playerPlayed    = 0;
        playerChoice    = 0;
       
    }



    /**************************************************************************/
    /**************************** HELPER FUNCTIONS ****************************/
    /**************************************************************************/

    // Return contract balance
    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }

    // Return player's ID
    function whoAmI() public view returns (uint) {
        if (msg.sender == playerA) {
            return 1;
        } if (msg.sender == HouseWallet) {
            return 0;
        }
    }


    modifier game_has_outcome() {
        require(outcome > 0);
        _;
    }

    function reset_contract() public game_has_outcome {

        initialBet      = 0;
        playerA         = address(0x0);
        HouseWallet     = address(0x0);
        outcome         = 0;
        paid            = 0;


    }
}



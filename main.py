#!/usr/bin/env python
from blockchain import Blockchain, build_list_of_validators, build_list_of_miners
from list_of_all_validators import ValidatorList
from list_of_all_miners import MinerList
from parameters import *
from random import randint

def main ():
    #Create a list of validators
    validator_list = build_list_of_validators(initial_validators)
    blockchain_validators = ValidatorList(validator_list)
    #Create a list of miners
    miner_list = build_list_of_miners(initial_miners)
    blockchain_miners = MinerList(miner_list)
    #Create the blockchain with the validators and miners lists
    my_blockchain = Blockchain(blockchain_validators, blockchain_miners)    
    number_of_transactions = 15
    #Make initial_users send own_coin transactions to each randomly
    for transaction in range(number_of_transactions):
        sender = randint(0, len(initial_users) - 1)
        receiver = randint(0, len(initial_users) - 1)
        owl_coins = randint(0, 100)
        #Checking that sender and reciever are different users with a while
        while sender == receiver:
            receiver = randint(0, len(initial_users))
        #Add vlaue to the blockchain until there are 5 and then a new block gets created
        my_blockchain.add_value(initial_users[sender][0]\
                                , initial_users[receiver][0]\
                                , owl_coins)
    print()
    print(my_blockchain)
    
if __name__ == '__main__':
    main()


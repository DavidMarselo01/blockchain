#IMPORTED MODULES
from datetime import datetime
import time
from hashlib import sha256
from random import randint, choices

"""
THINGS TO DO
1. Increment the age by day for each new block added
2. Actually add the block if there is consensus using the Block class
3. Voting mechanism/Vote class
4. "Printing" the blockchain if someone wants to see it
5. Slashing a person if they vote twice
6. self.transactions_per_block has to empty list after build_new_block is called
7. add parameters for age and weight in pick_winners() in ValidatorList
8. IMPORTANT: vote_proof() is the main thing for simulating consensus and it is primitive now
9. Related to 8, broadcastBlock() in proof_of_stake.py is primitive
"""


#MY_OTHER_FILES
from proof_of_work import *
from single_validator import *
from parameters import *
from proof_of_stake import *
from list_of_all_validators import *
from block import *
from vote import *

#BLOCKCHAIN CLASS
class Blockchain:
    def __init__(self, validators):
        #blockchain contains chain of blocks which have transactions
        self.blockchain = []
        #Tuples in transactions_per_block = (owls_coins_amount, From, To, Date)
        self.transactions_per_block = []
        self.validator_list = validators

    def last_block_hash(self):
        #means blockchain is empty
        if len(self) == 0:
            return ""
        else:
            return self.blockchain[-1].getHash()

    def __len__(self):
        return len(self.blockchain)

    def add_validator(self, validator):
        #takes Validator object as input
        self.validator_list.add_validator(validator)

    def build_new_block(self):
        #1. Create a new hash
        if len(self.blockchain) == 0:
            new_hash = create_hash("" + "".join(self.transactions_per_block[2]))
        else:
            new_hash = create_hash(self.blockchain[-1].getHash() + "".join(self.transactions_per_block[2]))
        #2. Reach Consensus on whether to add the block to the blockchain or not
        consensus_reached = False
        counter_mistakes = 0
        while consensus_reached == False:
            #1. pick a new winner from ValidatorList
            winner = (self.validator_list.pick_winner())[0]
            if (counter_mistakes == 0):
                print("Congratulations! The winner is", winner.name)
            else:
                print("Congratulations! The NEW winner is", winner.name, "lets try it again")
            #2. make winner mine the block
            proof = winner.mine(self.last_block_hash(), new_hash)
            #3. broadcast the block and get everyone to check it
            if (proof == 'Jibberish'):
                print("The broadcasted proof of work is wrong!")
            else:
                print("The broadcasted proof of work is",proof)
            
            block_has_consensus = broadcastBlock(self.validator_list.get_validators(),self.last_block_hash(), new_hash, str(proof))
            #4. check consensus of block
            if block_has_consensus[0]:
                print("This block was added")
                self.transactions_per_block.clear()
                consensus_reached = True
            elif(block_has_consensus[0] == False and block_has_consensus[1] == 'Proof of Work Incorrect'):
                print("This block was not added because hashing was done incorrectly\
                      , so we are going to choose a new winner")
                print('Punish ' + winner.name + 'by the amount staked')  
                counter_mistakes+=1
            else:
                print("This block was not added because less than 2/3 of validators said yes")
                print('Punish ' + winner.name + 'by the amount staked')
                counter_mistakes+=1

    def add_value(self, From, To, owls_coins_amount):
        time_stamp = str(datetime.now())[:19]
        #add value to new block
        self.transactions_per_block.append((str(owls_coins_amount), From, To,\
                                                                time_stamp))
            
        print(From.upper() + ' wants to send '+ str(owls_coins_amount) + \
              ' owls coins to ' + To.upper() + ' at ' + time_stamp)
        
        #after every 5 transactions, a new block is created
        if len(self.transactions_per_block) == amount_transactions_per_block:
            print("Creating new block now")
            self.build_new_block()

#users_data will contain a list of tuples as shown in the main() function
def build_list_of_validators(users_data):
    validator_list = []
    for user in users_data:
        validator = Validator(user[0], user[1])
        validator_list.append(validator)
    return validator_list

#MAIN
def main():
    #Tuples in initial_users (Name, money staked on each block, how long they
    #                                     were waiting to get picked a winner)
    
    initial_users = [
        ("Afnan", 22, 3),
        ("David", 13),
        ("Monplaisir", 17, 1),
        ("Claudia", 25, 1),
        ("Adam", 33, 1),
        ("James", 26, 2),
        ("Mercury", 22, 1),
        ("Hope", 12, 2),
        ("John", 29, 4),
        ("Jacob", 18, 2),
        ("Jesus", 20,4)
        ]
    validator_list = build_list_of_validators(initial_users)
    blockchain_validators = ValidatorList(validator_list)
    my_blockchain = Blockchain(blockchain_validators)
    
    number_of_transactions = 15
    for transaction in range(number_of_transactions):
        sender = randint(0, len(initial_users) - 1)
        receiver = randint(0, len(initial_users) - 1)
        owl_coins = randint(0, 100)
        #Checking that sender and reciever are different users with a while
        while sender == receiver:
            receiver = randint(0, len(initial_users))
        my_blockchain.add_value(initial_users[sender][0]\
                                , initial_users[receiver][0]\
                                , owl_coins)
    #20     
    # my_blockchain.add_value(3)
    # my_blockchain.add_value(13)
    # my_blockchain.add_value(17)
    # my_blockchain.add_value(13)
    
main()
    











        

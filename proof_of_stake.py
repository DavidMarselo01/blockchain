from single_validator import *
from hashlib import sha256

def broadcastBlock(lst_of_validators, last_hash, new_hash, proof):
    total_validators = len(lst_of_validators.validators)
    
    #get a count for how many votes it has
    votes = 0
    #we can somehow use these arrays containing who says yes and no to figure out
    #who should be punished or rewarded
    says_no = []
    says_yes = []
    for validator in lst_of_validators.validators:
        value = validator.vote_proof(last_hash, new_hash, proof)
        if value == 'Proof of Work Incorrect':
            return (False, 'Proof of Work Incorrect', '', '')
        if value == "no":
            says_no.append(validator)
            votes += 0
        elif value == "yes":
            says_yes.append(validator)
            votes += 1
        elif value == "offline":
            says_no.append(validator)
            votes += 0
    #check if two/thirds of all validators agree
    if votes >= total_validators*(3/5):
        return (True, 'All Correct', says_yes, says_no)
    else:
        return (False, 'Less than 2/3 of validators said yes', says_yes, says_no)
    

    


    
    
    
    
    
        
        
        

        
        

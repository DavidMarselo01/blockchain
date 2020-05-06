from single_validator import *
from hashlib import sha256

def broadcastBlock(lst_of_validators, last_hash, new_hash, proof):
    total_validators = len(lst_of_validators)
    if not checkProofOfWork(last_hash, new_hash, proof):
        return (False, 'Proof of Work Incorrect')
    #get a count for how many votes it has
    votes = 0
    #we can somehow use these arrays containing who says yes and no to figure out
    #who should be punished or rewarded
    says_no = []
    says_yes = []
    for validator in lst_of_validators:
        value = validator.vote_proof(last_hash, new_hash, proof)
        if value == "no":
            says_no.append(validator)
            votes += 0
        elif value == "yes":
            says_yes.append(validator)
            votes += 1
    #check if two/thirds of all validators agree
    if votes > total_validators*(2/3):
        return (True, 'All Correct')
    else:
        return (False, 'Less than 2/3 of validators said yes')
    

def checkProofOfWork(last_hash, new_hash, proof):
    input_to_sha256 = (last_hash + proof + new_hash).encode()
    check_hash = sha256(input_to_sha256).hexdigest()
    if (check_hash[:4] == '0000'):
        return True
    else:
        return False
    
        
        
        

        
        

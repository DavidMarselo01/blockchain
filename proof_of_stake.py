from single_validator import *
from hashlib import sha256

def broadcastBlock(lst_of_validators, last_hash, new_hash, proof):
    total_validators = len(lst_of_validators.validators)
    
    #get a count for how many votes it has to decide whether to approve a block or not
    votes = 0
    #Lists containing validators that approved or disapproved the block
    says_no = []
    says_yes = []
    check_if_all_validators_malicious_proof_of_work_incorrect = False
    for validator in lst_of_validators.validators:
        #For each validators, decide if block is approved or not
        value = validator.vote_proof(last_hash, new_hash, proof)
        #If Proof Of Work is incorrect we return False and the system chooses the next miner
        if value == 'Proof of Work Incorrect':
            return (False, 'Proof of Work Incorrect', '', '')
        #But validator can be malicious and say that proof of work is correct when in fact it is not
        elif value == 'Proof of Work Incorrect but validator is malicious':
            says_yes.append(validator)
            check_if_all_validators_malicious_proof_of_work_incorrect = True
            continue
        #Value can be no, because the validator is malicious or the block is malicious
        if value == "no":
            says_no.append(validator)
            votes += 0
        elif value == "yes":
            says_yes.append(validator)
            votes += 1
        elif value == "offline":
            says_no.append(validator)
            votes += 0
    #Check if all validators maliciously said yes, when proof of work is in fact incorrect
    if (check_if_all_validators_malicious_proof_of_work_incorrect == True):
        return (False, 'Proof of Work Incorrect', says_yes, says_no)
    #check if three/fifths of all validators agree
    if votes >= total_validators*(3/5):
        return (True, 'All Correct', says_yes, says_no)
    else:
        return (False, 'Less than 2/3 of validators said yes', says_yes, says_no)
    

    


    
    
    
    
    
        
        
        

        
        

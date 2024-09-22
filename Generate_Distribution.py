import random 
from Virtual_Values import Virtual_Values

def Generate_Distribution(type_space):
    
    for i in range(1000000):
        rands = [random.random() for i in range(len(type_space))]
        s = sum(rands)
        rands = [ i/s for i in rands ]
        vals = Virtual_Values.Virtual_Values(rands,type_space)
        sums = vals[-2]*(rands[-2]/sum(rands[-2:])) + (rands[-1]/sum(rands[-2:]))
        count = 0
        for j in range(len(type_space)-1):
            if vals[j+1] > vals[j]:
                count +=1
                if count == len(type_space)-3 and sums > vals[-3]:
                    return rands
            else:
                break
            
    return "No distribution found, try simulating again."

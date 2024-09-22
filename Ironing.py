import random 
import copy

def Ironing(distribution, type_space):
    v_v = Virtual_Values(distribution, type_space)
    original_vv = copy.deepcopy(v_v)

    for i in range(len(v_v)-1):
        start=0
        for j in range(1,len(v_v)):
            stop=j
            if v_v[start] > v_v[stop]:
                weight = [x/sum(distribution[start:stop+1]) for x in distribution[start:stop+1]]
                v_v[start:stop+1]= sum(original_vv[start:stop+1]*weight)           
            else:
                start+=1
        
    return v_v

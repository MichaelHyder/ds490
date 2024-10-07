from Ironing import Ironing
import numpy as np

def Flow(type_space, distribution, flows):
    ironed = Ironing(distribution,type_space)
    ironed = np.insert(ironed,0,0)
    type_space = [0] + type_space
    initial_lagrangian =[0.0]* len(type_space)
    ans_ironed = 0
    ans_lagrangian = 0
    
    for i in range(len(type_space)): 
        for j in range(len(type_space)):
            initial_lagrangian[i] += (flows[j][i])*(i - j)
    
    
    lagrangian = [initial_lagrangian[i+1] * 1/distribution[i] for i in range(len(initial_lagrangian)-1)]
    
    lagrangian = [0] + lagrangian
    distribution = [0] + distribution
    
    for v_1 in range(len(type_space)):
        for v_2 in range(v_1 + 1,len(type_space)):
            if ironed[v_1] < ironed[v_2]:
                ans_ironed += distribution[v_1] * distribution[v_2] * ironed[v_2]
            else: 
                ans_ironed += distribution[v_1] * distribution[v_2] * ironed[v_1]
                
            if lagrangian[v_1] < lagrangian[v_2]:
                ans_lagrangian += distribution[v_1] * distribution[v_2] * lagrangian[v_2]
            else: 
                ans_lagrangian += distribution[v_1] * distribution[v_2] * lagrangian[v_1]
            
    if round(ans_ironed,4) + 0.0001 >= round(ans_lagrangian,4)  >= round(ans_ironed,4) - 0.0001:
        print("They are equal! This is optimal! The value is", round(ans_ironed,4))
    else:
        print("They are not equal! This is not optimal! The ironed value is", round(ans_ironed,4)) 
        print("The lagrangian value is", round(ans_lagrangian,4))
    return

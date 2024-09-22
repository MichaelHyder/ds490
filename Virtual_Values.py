def cdf(array,i):
    ans = 0
    for pdf in array[i:]:
        ans += pdf
        
    return ans

def Theta(distribution,type_space,i):
    f= np.array(distribution)
    t= np.array(type_space)
    virt_val = t[0]/f[0]
    if i == 0:
        return virt_val
    else:
        return ((t[i]-t[i-1])*cdf(f, i))/f[i]

def Virtual_Values(distribution, type_space):
    
    virt_values = np.array([])
    for i in range(len(distribution)):
        virt_values = np.append(virt_values, Theta(distribution, type_space, i))
        
    return virt_values

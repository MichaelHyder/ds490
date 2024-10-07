from Matrix import Matrix
from Flow import Flow

def Verify():
    type_space_input = input("Enter your type space separated by commas. Do NOT include the source (e.g., 1,2,3,4,5): ")
    type_space = [float(num) for num in type_space_input.split(",")] 
    
    while True:
            try:
                distribution_input = input("Enter your distribution separated by commas (e.g., 0.2,0.2,0.2,0.2,0.2): ")
                distribution = [eval(num) for num in distribution_input.split(",")] 
                if len(distribution)==len(type_space) and 1.000001 > sum(distribution) > 0.999999:
                    break  
                elif 0.999999 > sum(distribution) or sum(distribution) > 1.000001:
                    print("The distribution needs to have a sum equal to 1. Please enter a new distribution.")
                else:
                    print("The distribution needs the same number of values as the type space. Please enter a new distribution.")

            except ValueError:
                  print("Invalid Input")
            continue
        
    matrix = Matrix(type_space)
    
    return Flow(type_space, distribution, matrix)

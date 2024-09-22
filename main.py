def main():
    type_space_input = input("Enter your type space separated by commas (e.g., 1,2,3,4,5): ")
    type_space = [float(num) for num in type_space_input.split(",")] 
    
    choice = input("Do you have a distribution to enter? If so, type yes, if not, type no: ")
    if choice == "yes" or choice == "Yes":
        while True:
            try:
                distribution_input = input("Enter your distribution separated by commas (e.g., 0.2,0.2,0.2,0.2,0.2): ")
                distribution = [float(num) for num in distribution_input.split(",")] 
                if len(distribution)==len(type_space) and 1.000001 > sum(distribution) > 0.999999:
                    break  
                elif 0.999999 > sum(distribution) or sum(distribution) > 1.000001:
                    print("The distribution needs to have a sum equal to 1. Please enter a new distribution.")
                else:
                    print("The distribution needs the same number of values as the type space. Please enter a new distribution.")

            except ValueError:
                  print("Invalid Input")
            continue
        
    elif choice == "no" or choice == "No":
        print("Your distribution will be generated, this might take a moment.")
        distribution = Generate_Distribution.Generate_Distribution(type_space)
        print("Here is your distribution! ", distribution)
        
    else:
        print("You need a distribution! A distriubtion will be generated for you now, this might take a moment.")
        distribution = Generate_Distribution.Generate_Distribution(type_space)
        print("Here is your distribution! ", distribution)
    
    choice_2 = input("Do you want to see the virtual values of this distribution? If so, type yes, if not, type no: ")
    if choice_2 == "yes" or choice == "Yes":
        vv = Virtual_Values.Virtual_Values(distribution,type_space)
        print("Here are your virtual values! ", vv)
        
    choice_3 = input("Do you need this ironed? If so, type yes, if not, type no: ")
    if choice_3 == "yes" or choice == "Yes":
        ironed = Ironing.Ironing(distribution,type_space)
        return "Here are your ironed values!", ironed

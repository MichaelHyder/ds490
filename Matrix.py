def create_zero_matrix(size):
    return [[0 for _ in range(size)] for _ in range(size)]

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

def replace_value(matrix, row, col, value):
    if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
        matrix[row][col] = value
    else:
        print("Invalid index!")

def Matrix(type_space):
    size = len(type_space)+1
    matrix = create_zero_matrix(size)
    
    print("Initial matrix:")
    print_matrix(matrix)
    
    while True:
        row = int(input("Enter the row index to replace (or -1 to exit): "))
        if row == -1:
            break
        col = int(input("Enter the column index to replace: "))
        value = input("Enter the new value: ")
        evaluate = round(eval(value), 4)
        print(evaluate)
        
        replace_value(matrix, row, col, evaluate)
        
        print("Updated matrix:")
        print_matrix(matrix)
    
    return matrix

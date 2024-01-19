def simplex_minimize(obj_vars_count, constraints, objective_function):
    matrix, artif_rows = construct_matrix(obj_vars_count, constraints)
    rows, cols = len(matrix), len(matrix[0])  # matrix dimensions
    basic_vars = [0 for _ in range(rows)]  # array of basic variables indices
    s_index = obj_vars_count  # index of slack variables
    a_index = obj_vars_count + slack_vars_count  # index of artificial variables

    # phase 1
    for i in range(a_index, cols - 1):  # setting artificial vars to -1
        matrix[0][i] = -1
    for i in artif_rows:
        matrix[0] = [matrix[0][j] + matrix[i][j] for j in range(cols)]
        basic_vars[i] = a_index
        a_index += 1

    for i in range(1, len(basic_vars)):
        if basic_vars[i] == 0:
            basic_vars[i] = s_index
            s_index += 1

    # run simplex iterations
    run_iterations(matrix, basic_vars)
    # phase 1 ends

    # delete artificial vars
    for i in range(rows):
        length = obj_vars_count + slack_vars_count + 1  # row length without artificial vars
        while len(matrix[i]) != length:
            matrix[i].pop(length - 1)  # delete artificial var

    # phase 2
    for i in range(obj_vars_count):  # insert objective function coefficients into matrix with opposite sign
        matrix[0][i] = -objective_function[i]

    for row, col in enumerate(basic_vars[1:]):
        if matrix[0][col] != 0:
            tmp = [-matrix[0][col] * x for x in matrix[row + 1]]
            matrix[0] = [matrix[0][j] + tmp[j] for j in range(len(tmp))]

    # run simplex iterations
    run_iterations(matrix, basic_vars)
    # phase 2 ends

    # constructing solution
    solution = {var: matrix[i + 1][-1] for i, var in enumerate(basic_vars[1:]) if var < obj_vars_count}

    for var in range(obj_vars_count):
        if var not in basic_vars[1:]:
            solution[var] = 0

    return solution, matrix[0][-1]


def construct_matrix(var_count, constraints):
    matrix = [[0 for _ in range(var_count + slack_vars_count + artif_vars_count + 1)]
              for __ in range(len(constraints) + 1)]  # initialising empty matrix
    s_index = var_count  # index of slack variables
    a_index = var_count + slack_vars_count  # index of artificial variables
    artif_rows = []  # indices of rows with artificial vars

    for i in range(1, len(constraints) + 1):
        constraint = constraints[i - 1]
        for j in range(len(constraint) - 2):
            matrix[i][j] = constraint[j]

        if constraint[-1] == '<=':
            matrix[i][s_index] = 1  # add slack variable
            s_index += 1  # increment slack var index
        elif constraint[-1] == '=':
            matrix[i][a_index] = 1  # add artificial variable
            a_index += 1  # increment artificial var index
            artif_rows.append(i)  # add row to the list

        matrix[i][-1] = constraint[-2]  # add constraint right hand side to the matrix
    return matrix, artif_rows


def find_pivot_row(matrix, pivot_column):
    min_val = float('inf')
    min_i = 0
    for i in range(1, len(matrix)):
        if matrix[i][pivot_column] > 0:
            val = matrix[i][-1] / matrix[i][pivot_column]
            if val < min_val:
                min_val = val
                min_i = i
    return min_i


def run_iterations(matrix, basic_vars):
    rows, cols = len(matrix), len(matrix[0])  # matrix dimensions
    pivot_column = matrix[0][:-1].index(max(matrix[0][:-1]))  # get index of maximal element in objective function row

    while matrix[0][pivot_column] > 0:
        pivot_row = find_pivot_row(matrix, pivot_column)
        basic_vars[pivot_row] = pivot_column
        pivot = matrix[pivot_row][pivot_column]  # get pivot element

        # normalize pivot row
        for i in range(cols):
            matrix[pivot_row][i] /= pivot

        # nullify pivot column
        for i in range(rows):
            if i != pivot_row:
                factor = matrix[i][pivot_column]
                for j in range(cols):
                    matrix[i][j] -= matrix[pivot_row][j] * factor

        pivot_column = matrix[0][:-1].index(max(matrix[0][:-1]))


# x11 x12 x13 ... x54
obj_function_coefs = [10, 20, 40, 60, 30, 30, 10, 15, 50, 35, 20, 30, 70, 45, 15, 20, 20, 65, 30, 60]

# x11 x12 x13 ... x54 b constraint_sign
constraints = ([1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1000, '='],
               [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 500, '='],
               [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 200, '='],
               [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 300, '='],
               [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 500, '<='],
               [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 300, '<='],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 700, '<='],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 250, '<='],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 750, '<='])
obj_vars_count = 20  # number of objective function variables
slack_vars_count = 5  # number of slack variables to be added
artif_vars_count = 4  # number of artificial variables to be added

solution, optimize_val = simplex_minimize(obj_vars_count, constraints, obj_function_coefs)

print(optimize_val)
for i in range(len(solution)):
    print(f'x_{i // 4 + 1}{i % 4 + 1} = {solution[i]}')

# Solving a Sudoku by modeling it as a boolean satisfiability problem. Also generating a sudoku.cnf file for use with other sat solvers

# Assign p boolean variables to each cell in the pxp matrix that represents the sudoku.
# So the p boolean variables are analogous to a one-hot encoding for the value of a particular cell.
# Now, to formulate the clauses for this satisfiability problem and pass them into the sat solver
# Note, that the clauses will have p*p*p boolean variables


# i, j vary from 0 to 8 each

import copy, pycosat


def set_params(sudo_sz):
	global sudo_size, sudo_size_square, sudo_size_sqrt;
	sudo_size= sudo_sz;
	sudo_size_square = int(sudo_size ** 2) ;
	sudo_size_sqrt = int(sudo_size ** 0.5);

def v(i,j,k): # Given index i,j and value k, it gives the boolean variable number for i,j having value k, as per the one-hot encoding
	return (sudo_size_square)*i+(sudo_size)*j+k

def element_clause(clause_set):
	# Uniqueness: one cell only points to one value
	for i in range(sudo_size):
		for j in range(sudo_size):
			# This is the clause that states that atleast one of the p boolean variables must be true
			clause_set.append([v(i,j,d) for d in range(1,(sudo_size+1))])
			# Following is the set of clauses that state that no two(or more) of these boolean variables can be true
			for d in range(1,(sudo_size+1)):
				for dp in range(d+1,(sudo_size+1)):
					clause_set.append([-v(i,j,d), -v(i,j,dp)])
	return clause_set
	
def row_clause(i,clause_set):
	# A row of the matrix must contain each of the p values.
	# The condition is implemented as the sum of the kth boolean variable for each element in the row is exactly 1 (k=1:p)
	for k in range(1,(sudo_size+1)):
		temp = range(sudo_size_square*i+k, sudo_size_square*(i+1)+1, sudo_size)
		clause_set.append(temp)
	return clause_set

def col_clause(j,clause_set):
	# A column of the matrix must contain each of the p values
	# The condition is implemented as the sum of the kth boolean variable for each element in the column is exactly 1 (k=1:p)
	for k in range(1,(sudo_size+1)):
		temp = range(sudo_size*j+k, sudo_size_square*(sudo_size-1) + sudo_size*(j+1)+1, sudo_size_square)
		clause_set.append(temp)
	return clause_set

def block_clause(i,j,clause_set):
	# For each block starting at (i,j), the block contains each of the p values.
	# Similar formulation to the row and column clauses
	for k in range(1,(sudo_size+1)):
		temp = []
		for k1 in range(sudo_size_sqrt):
			for k2 in range(sudo_size_sqrt ):
				temp.append(v(i+k1,j+k2,k))
		clause_set.append(temp)
	return clause_set
	
def sudoku_vals(sudoku_mat):
	# Considering the given values in the sudoku. These get added to the clause set as singleton clauses (must always be true)
	clause_set = []
	for i in range(1,(sudo_size+1)):
		for j in range(1, (sudo_size+1)):
			val = sudoku_mat[i-1][j-1]
			if val:
				clause_set.append([v(i-1,j-1,val)])
	return clause_set
	
def print_sudoku(sudoku_mat):
	for i in sudoku_mat:
		print i;
	
def solve(sudoku_mat, sudoku_sz):
	# Setting params (size, size-square, root-size)
	set_params(sudoku_sz)
	# Adding all clauses to the list clause_set
	clause_set = sudoku_vals(sudoku_mat);
	for i in range(sudo_size):
		row_clause(i, clause_set)
		col_clause(i, clause_set)
	element_clause(clause_set)
	for i in range(sudo_size_sqrt):
		for j in range(sudo_size_sqrt):
			block_clause(i*sudo_size_sqrt,j*sudo_size_sqrt,clause_set)
	print len(clause_set)
	# We would also like to print a cnf file 'sudoku.cnf' of the clauses so we canconveniently use it with other SAT solvers
	outfile = file('sudoku.cnf','w')
	outfile.write('p cnf '+str(sudo_size**3)+' '+str(len(clause_set)))
	for clause in clause_set:
		string = ''
		for var in clause:
			string = string + str(var) + ' '
		string = string[:-1]
		outfile.write('\n'+string+' 0')
	# Solving the sudoku using pycosat SAT solver for python, which is based on PicoSAT
	sol = set(pycosat.solve(clause_set))
	# Editing the original matrix to reflect the solved sudoku
	def read_cell(i,j):
		for d in range(1,sudo_size+1):
			if v(i,j,d) in sol:
				return d
	
	for i in range(sudo_size):
		for j in range(sudo_size):
			sudoku_mat[i][j] = read_cell(i,j)


if __name__ == '__main__':
	from pprint import pprint
	# Comment out one of the following two matrices, depending on what size of matrix you want to use.
	sudoku_mat = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]]
	#~ sudoku_mat = [[1, 0, 0, 0],
            #~ [0, 2, 1, 0],
            #~ [0, 0, 3, 0],
            #~ [0, 0, 0, 4]]
	solve(sudoku_mat, len(sudoku_mat))
	print_sudoku(sudoku_mat)



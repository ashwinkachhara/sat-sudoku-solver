# i, j vary from 0 to 8 each

import copy, pycosat

def v(i,j,k):
	return 81*i+9*j+k

def element_clause(i,j,clause_set):
	# Uniqueness: one cell only points to one value
	base = range(-81*i-9*j-9, -81*i-9*j)
#	clause_set = []
	for k in range(0,9):
		temp = copy.deepcopy(base)
		temp[k] = -1*temp[k]
		clause_set.append(temp)
	return clause_set
	
def row_clause(i,clause_set):
#	clause_set = []
	for k in range(1,10):
		temp = range(81*i+k, 81*(i+1)+1, 9)
		clause_set.append(temp)
	return clause_set

def col_clause(j,clause_set):
#	clause_set = []
	for k in range(1,10):
		temp = range(9*j+k, 81*8 + 9*(j+1)+1, 81)
		clause_set.append(temp)
	return clause_set

def block_clause(i,j,clause_set):
#	clause_set = []
	for k in range(1,10):
		temp = []
		for k1 in range(3):
			for k2 in range(3):
				temp.append(v(i+k1,j+k2,k))
		clause_set.append(temp)
	return clause_set
	
def sudoku_vals(sudoku_mat):
	clause_set = []
	for i in range(1,10):
		for j in range(1, 10):
			val = sudoku_mat[i-1][j-1]
			if val:
				clause_set.append([v(i-1,j-1,val)])
	return clause_set
	
def solve(sudoku_mat):
	clause_set = sudoku_vals(sudoku_mat);
	for i in range(9):
		row_clause(i, clause_set)
		col_clause(i, clause_set)
		for j in range(9):
			element_clause(i,j, clause_set)
	block_clause(0,0,clause_set)
	block_clause(0,3,clause_set)
	block_clause(0,6,clause_set)
	block_clause(3,0,clause_set)
	block_clause(3,3,clause_set)
	block_clause(3,6,clause_set)
	block_clause(6,0,clause_set)
	block_clause(6,3,clause_set)
	block_clause(6,6,clause_set)
	print clause_set
	sol = set(pycosat.solve(clause_set))
	#print sol
	
	def read_cell(i,j):
		for d in range(1,10):
			if v(i,j,d) in sol:
				return d
	
	for i in range(9):
		for j in range(9):
			sudoku_mat[i][j] = read_cell(i,j)
	

if __name__ == '__main__':
	#block_clause(6,6)
	hard = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]]
	solve(hard)
	#print(hard)

# i, j vary from 0 to 8 each

import copy, pycosat


def set_params(sudo_sz):
	global sudo_size, sudo_size_square, sudo_size_sqrt;
	sudo_size= sudo_sz;
	sudo_size_square = int(sudo_size ** 2) ;
	sudo_size_sqrt = int(sudo_size ** 0.5);

def v(i,j,k):
	return (sudo_size_square)*i+(sudo_size)*j+k

def element_clause(clause_set):
	# Uniqueness: one cell only points to one value
	for i in range(sudo_size):
		for j in range(sudo_size):
			clause_set.append([v(i,j,d) for d in range(1,(sudo_size+1))])
			for d in range(1,(sudo_size+1)):
				for dp in range(d+1,(sudo_size+1)):
					clause_set.append([-v(i,j,d), -v(i,j,dp)])
	return clause_set
	
def row_clause(i,clause_set):
#	clause_set = []
	for k in range(1,(sudo_size+1)):
		temp = range(sudo_size_square*i+k, sudo_size_square*(i+1)+1, sudo_size)
		clause_set.append(temp)
	return clause_set

def col_clause(j,clause_set):
#	clause_set = []
	for k in range(1,(sudo_size+1)):
		temp = range(sudo_size*j+k, sudo_size_square*(sudo_size-1) + sudo_size*(j+1)+1, sudo_size_square)
		clause_set.append(temp)
	return clause_set

def block_clause(i,j,clause_set):
#	clause_set = []
	for k in range(1,(sudo_size+1)):
		temp = []
		for k1 in range(sudo_size_sqrt):
			for k2 in range(sudo_size_sqrt ):
				temp.append(v(i+k1,j+k2,k))
		clause_set.append(temp)
	return clause_set
	
def sudoku_vals(sudoku_mat):
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
	set_params(sudoku_sz)
	clause_set = sudoku_vals(sudoku_mat);
	for i in range(sudo_size):
		row_clause(i, clause_set)
		col_clause(i, clause_set)
	element_clause(clause_set)
	for i in range(sudo_size_sqrt):
		for j in range(sudo_size_sqrt):
			block_clause(i*sudo_size_sqrt,j*sudo_size_sqrt,clause_set)
	print len(clause_set)
	outfile = file('sudoku.cnf','w')
	outfile.write('p cnf '+str(sudo_size**3)+str(len(clause_set)))
	for clause in clause_set:
		string = ''
		for var in clause:
			string = string + str(var) + ' '
		string = string[:-1]
		outfile.write('\n'+string+' 0')
	sol = set(pycosat.solve(clause_set))
	#print sol
	
	def read_cell(i,j):
		for d in range(1,sudo_size+1):
			if v(i,j,d) in sol:
				return d
	
	for i in range(sudo_size):
		for j in range(sudo_size):
			sudoku_mat[i][j] = read_cell(i,j)


if __name__ == '__main__':
	#block_clause(6,6)
	from pprint import pprint
	
	#~ hard = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
            #~ [0, 0, 0, 6, 0, 0, 0, 0, 3],
            #~ [0, 7, 4, 0, 8, 0, 0, 0, 0],
            #~ [0, 0, 0, 0, 0, 3, 0, 0, 2],
            #~ [0, 8, 0, 0, 4, 0, 0, 1, 0],
            #~ [6, 0, 0, 5, 0, 0, 0, 0, 0],
            #~ [0, 0, 0, 0, 1, 0, 7, 8, 0],
            #~ [5, 0, 0, 0, 0, 9, 0, 0, 0],
            #~ [0, 0, 0, 0, 0, 0, 0, 4, 0]]
	hard = [[1, 0, 0, 0],
            [0, 2, 1, 0],
            [0, 0, 3, 0],
            [0, 0, 0, 4]]
	solve(hard, len(hard))
	print_sudoku(hard)
	#~ assert [[1, 2, 6, 4, 3, 7, 9, 5, 8],
            #~ [8, 9, 5, 6, 2, 1, 4, 7, 3],
            #~ [3, 7, 4, 9, 8, 5, 1, 2, 6],
            #~ [4, 5, 7, 1, 9, 3, 8, 6, 2],
            #~ [9, 8, 3, 2, 4, 6, 5, 1, 7],
            #~ [6, 1, 2, 5, 7, 8, 3, 9, 4],
            #~ [2, 6, 9, 3, 1, 4, 7, 8, 5],
            #~ [5, 4, 8, 7, 6, 9, 2, 3, 1],
            #~ [7, 3, 1, 8, 5, 2, 6, 4, 9]] == hard


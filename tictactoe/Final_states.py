import numpy as np
import re
from itertools import combinations
from TicTacToeLogic import Board,Read_states_from_file_py


N = Board.SIZE


def Calculate_states(n,show_states=False):
	all_states = set()
	#rotation_flip = set()
	for i in range(n,2*n):
		comb = combinations(range(n**2),i)
		for c in comb:
			#print c
			b = Board(n,1)
			for ci in c:
				b.pieces.ravel()[ci] = 0
			if not b.is_win(1) and len(b.get_legal_moves(False)) == 0:
				if show_states:
					all_states.add(str(b.pieces.ravel()))
				else:
					rotation_flip = set()

					for r in range(1,5):
						for f in [True, False]:
							rot = np.rot90(b.pieces,r)
							if f:
								rot = np.fliplr(rot)

							rotation_flip.add(str(rot.ravel()))
					if (rotation_flip & all_states) == set([]):
						all_states.add(str(b.pieces.ravel()))
   	return all_states

def Write_states_to_file(filename):
	all_states =  Calculate_states(Board.SIZE)
	f = open(filename, "w")
	for i in all_states:
		f.write(i.strip('[]')+'\n')
	f.close()



def main():
	
	# print np.where(b.pieces == 0)
	#all_states =  Calculate_states(Board.SIZE)
	filename = 'states_'+str(Board.SIZE) + 'x' + str(Board.SIZE) + '.txt'
	#Write_states_to_file(filename)
	print len(Calculate_states(5,True))
	#a = Read_states_from_file_py(filename)
	# a_list = [k.pieces for k in a]
	# b = a_list.pop()

	# small_list=[]
	# for r in range(1,5):
	# 	for f in [True, False]:
	# 		rot = np.rot90(b,r)
	# 		if f:
	# 			rot = np.fliplr(rot)

	# 		small_list.append(rot)
	# print [value for value in small_list if value in a_list]



  
if __name__== "__main__":
    main()

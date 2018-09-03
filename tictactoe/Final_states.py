import numpy as np
import re
from itertools import combinations
from TicTacToeLogic import Board

N = Board.SIZE


def Calculate_states(n):
	all_states = set()
	#rotation_flip = set()
	for i in range(n,2*n):
		comb = combinations(range(n**2),i)
		for c in comb:
			#print c
			b = Board(N,1)
			for ci in c:
				b.pieces.ravel()[ci] = 0
			#print b
			if not b.is_win(1) and len(b.get_legal_moves(False)) == 0:
				#print b
				#print b
				rotation_flip = set()

				for r in range(1,5):
					for f in [True, False]:
						rot = np.rot90(b.pieces,r)
						if f:
							rot = np.fliplr(rot)

						rotation_flip.add(str(rot))
				#print 'rotation_flip:',rotation_flip
				#print('rotation_flip & all_states', rotation_flip & all_states)
				if (rotation_flip & all_states) == set([]):
					all_states.add(str(b.pieces))

				# if str(b.pieces) not in rotation_flip:
				# 	print b 
				# 	all_states.add(b)
	#print 'all_states:',all_states
   	return all_states

def initial_board(n):
    return np.ones([n,n])

#def validate_states:











def main():
	
	b = Board(N,1)
	# all_states.add(b)
	# print all_states
	# b =Board(3,1)
	b.pieces = np.array([[1, 1, 0],[1, 0, 1],[0, 1, 1]])
	# print np.where(b.pieces == 0)
	all_states =  Calculate_states(Board.SIZE)
	#print np.rot90(b.pieces,4)
	#print b


	#print [i for i in all_states]






	#print b.get_legal_moves(True)
	#all_states = Calculate_states(N)
	#print [b.pieces for b in all_states]
	print len(all_states)
    #print all_states


  
if __name__== "__main__":
    main()

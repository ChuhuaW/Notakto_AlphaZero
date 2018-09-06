from copy import deepcopy
import re
import numpy as np
'''
Board class for the game of TicTacToe.
Default board size is 3x3.
Board data:
  1=white(O), -1=black(X), 0=empty
  first dim is column , 2nd is row:
     pieces[0][0] is the top left square,
     pieces[2][0] is the bottom left square,
Squares are stored and manipulated as (x,y) tuples.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the board for the game of Othello by Eric P. Nichols.

'''
# from bkcharts.attributes import color

class Board():

    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
    SIZE = 4
    def __init__(self, n=SIZE, initial = 0):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [initial]*self.n
        self.pieces = np.array(self.pieces)
        self.mask_pieces=[]


    def __str__(self):
        return str(self.pieces)

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        #print('Tgus us index', index,self.pieces)
        return self.pieces[index]

    def get_mask_pieces(self):
        ind = np.where(self.pieces==0)
        self.mask_pieces = [(ind[0][i],ind[1][i]) for i in range(ind[0].shape[0])]


    def get_legal_moves(self,final=True,valid = True):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.        
        """
        moves = set()  # stores the legal moves.
        states_to_moves = {}

        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                # if the piece is removed in leaf based search, mask it
                if self[x][y]==0 and (x,y) not in self.mask_pieces:
                    newmove = (x,y)
                    moves.add(newmove)
        # following codes is to ignore suicide moves
        moves = list(moves)
        #print self.pieces
        copy = deepcopy(self)
        all_possible_states = []
        for m in moves:
            self = deepcopy(copy)
            self.execute_move(m,1)
            states_to_moves[str(self)]=m

            all_possible_states.append(self)
        if valid == True:
            all_possible_states = self.validatePossibleMoves(all_possible_states,final)
        # print('all_possible_states',all_possible_states)
        # print(states_to_moves[str(all_possible_states[0])])
        # print('length of states',len(all_possible_states))
        if all_possible_states ==[]:
            mask_pieces = deepcopy(copy.mask_pieces)
            copy.mask_pieces = []
            return mask_pieces
        self = deepcopy(copy)

        return [states_to_moves[str(s)] for s in all_possible_states]

    def validatePossibleMoves(self,all_possible_states,final):
        winners = []
        for state in all_possible_states:
            winners.append(state.is_win(1))
        if final:
            if all(win == True for win in winners):
                return all_possible_states
            else:
                return [all_possible_states[w] for w in range(len(winners)) if winners[w] == 0]
        else:
            if all(win == True for win in winners):
                return []
            else:
                return [all_possible_states[w] for w in range(len(winners)) if winners[w] == 0]      

    def Randomly_remove(self, depth = 2):
        '''
        remove pieces from board in random based on depth
        '''

        #print 'board:',self
        # return array of index of all pieces on the board and
        #state_copy = np.copy(self.pieces)
        indice = np.where(self.pieces == 1)
        depth = int(self.pieces.sum()/2)
        #print 'indice', indice
        # choose (depth) index at random
        removed_indice = np.random.choice(indice[0].shape[0],depth,replace=False)
        for i in removed_indice:
            x,y = indice[0][i], indice[1][i]
            #print x,y
            self[x][y]=0
        return self

    def All_remove(self):
        '''
        remove pieces from board in random based on depth
        '''

        #print 'board:',self
        # return array of index of all pieces on the board and
        #state_copy = np.copy(self.pieces)
        self.pieces = np.zeros(Board.SIZE,Board.SIZE)
        return self

    def has_legal_moves(self):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    return True
        return False
    
    def is_win(self, color):
        """Check whether the given player has collected a triplet in any direction; 
        @param color (1=white,-1=black)
        """
        color = 1
        win = self.n
        # check y-strips
        for y in range(self.n):
            count = 0
            for x in range(self.n):
                if self[x][y]==color:
                    count += 1
            if count==win:
                return True
        # check x-strips
        for x in range(self.n):
            count = 0
            for y in range(self.n):
                if self[x][y]==color:

                    count += 1
            if count==win:
                return True
        # check two diagonal strips
        count = 0
        for d in range(self.n):
            if self[d][d]==color:
                count += 1
        if count==win:
            return True
        count = 0
        for d in range(self.n):
            if self[d][self.n-d-1]==color:
                count += 1
        if count==win:
            return True
        
        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        (x,y) = move

        # Add the piece to the empty square.
        assert self[x][y] == 0
        self[x][y] = 1


def Read_states_from_file(filename):
    '''read states from files and convert them into Board()'''
    f=open(filename, "r")
    states = f.read().strip('\n').split('\n\n')
    boards_array = []
    for s in states:
        s = re.sub('\n','',s)
        b = Board()
        b.pieces = np.array(list(s), dtype=int).reshape(Board.SIZE,Board.SIZE)
        b.get_mask_pieces()
        boards_array.append(b)
    return boards_array

def Read_states_from_file_py(filename):
    '''read states from files and convert them into Board()'''
    f=open(filename, "r")
    states = f.read().strip('\n').split('\n')
    #f.write(str(np.fromstring(i.strip('[]'),dtype=int, sep=' '))+'\n')
    #print states
    boards_array = []
    for s in states:
        b = Board()
        b.pieces = np.fromstring(s,dtype=int, sep=' ').reshape(Board.SIZE,Board.SIZE)
        #b.get_mask_pieces()
        boards_array.append(b)
    return boards_array

#b = Board()
#b.pieces=np.array([[1,0,1],[1,1,1],[1,1,0]])

#b.pieces = np.zeros(Board.SIZE,Board.SIZE)

# print b.pieces.sum()
# b.Randomly_remove()
# print 'before',b.mask_pieces
# # print b.pieces[3]
# #print b.get_mask_pieces()
# b.get_mask_pieces()
# b.pieces=np.array([[0,0,1],[1,0,1],[1,1,0]])
#print b.get_legal_moves()
# print 'after',b2.mask_pieces

# #b.pieces[0][0]=1
# b.pieces[0][1]=1
# b.pieces[1][0]=1
# print('b.pieces',b.pieces)
#print(b.get_legal_moves(1))

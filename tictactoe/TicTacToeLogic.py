from copy import deepcopy
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
    SIZE=4
    def __init__(self, n=SIZE):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.        
        """
        moves = set()  # stores the legal moves.
        states_to_moves = {}

        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
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
        #print('self.pieces',self.pieces)
            all_possible_states.append(self)
        #print('all_possible_states,',[all_possible_states[s].pieces for s in range(len(all_possible_states))])
        #print(len(all_possible_states))
        all_possible_states = self.validatePossibleMoves(all_possible_states)
        #print('all,',[all_possible_states[s].pieces for s in range(len(all_possible_states))])
        #print(len(all_possible_states))

        self = deepcopy(copy)
        #print('newmove:',[states_to_moves[str(s)] for s in all_possible_states])
        #print('self',self.pieces)
        return [states_to_moves[str(s)] for s in all_possible_states]

    def validatePossibleMoves(self,all_possible_states):
        winners = []
        for state in all_possible_states:
            winners.append(state.is_win(1))
        if all(win == True for win in winners):
            return all_possible_states
        else:
            return [all_possible_states[w] for w in range(len(winners)) if winners[w] == 0]

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

# b = Board(3)
# b.pieces[1][1]=1
# #b.pieces[0][0]=1
# b.pieces[0][1]=1
# b.pieces[1][0]=1
# print('b.pieces',b.pieces)
#print(b.get_legal_moves(1))

import numpy as np
import re



def Calculate_states():
    return

def Create_board(n):
    return np.ones(n,n)

def Read_states_from_file(filename):
    f=open(filename, "r")
    states = f.read().strip('\n').split('\n\n')
    states_array = []
    for s in states:
        s = re.sub('\n','',s)
        states_array.append(np.array(list(s), dtype=int).reshape(3,3))
    return states_array

def Randomly_remove(state, depth = 2):
    '''
    remove pieces from board in random based on depth
    '''

    # return array of index of all pieces on the board and
    state_copy = np.copy(state)
    indice = np.where(state_copy == 1)
    # choose (depth) index at random
    remove_indice = np.random.choice(indice[0].shape[0],depth,replace=False)
    for i in remove_indice:
        x,y = indice[0][i], indice[1][i]
        state_copy[x][y]=0
    return state_copy







def main():
    state = Read_states_from_file("states.txt")
    print state[0]
    #print np.where(state[0] == 1)
    print Randomly_remove(state[0])
  
if __name__== "__main__":
    main()

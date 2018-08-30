import numpy as np
import re
import TicTacToeLogic as logic



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

def Randomly_remove(state,depth=1):
    indice = np.where(state == 1)
    #array_range = state.shape[0]**2
    remove_indice = np.random.choice(indice[0].shape[0],depth,replace=False)
    for i in remove_indice:
        x,y = indice[0][remove_indice][0], indice[1][remove_indice][0]
        state[x][y]=0
    return state








def main():
    state = Read_states_from_file("states.txt")
    print state[0]
    #print np.where(state[0] == 1)
    Randomly_remove(state[0])
  
if __name__== "__main__":
    main()

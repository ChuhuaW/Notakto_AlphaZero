# from Coach import Coach
# from othello.OthelloGame import OthelloGame as Game
# from othello.pytorch.NNet import NNetWrapper as nn
# from utils import *

from Coach import Coach
from tictactoe.TicTacToeGame import TicTacToeGame
from tictactoe.TicTacToeLogic import Board
from tictactoe.keras.NNet import NNetWrapper as nn
from utils import *



args = dotdict({
    'numIters': 1,
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,

    'leaf_based_sampling': True,
    'random_iterations': 1,
    'states_file': './tictactoe/states.txt',
    'numItersForLeafNodeSearch': 10,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/','best3x3.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__=="__main__":
    #g = Game(6)
    g = TicTacToeGame(Board.SIZE)
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()

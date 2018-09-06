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
    'numIters': 70,
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 20000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,

    'leaf_based_sampling': True,
    'random_iterations': 1,
    'states_file': './tictactoe/states_4x4.txt',
    'remove_depth': 10,

    'checkpoint': './temp/4x4/',
    'load_model': False,
    'load_folder_file': ('/nfs/zapdos/home/data/vision3/cw234/tictactoe/alpha-zero-general/temp/','best_4x4.pth.tar'),
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

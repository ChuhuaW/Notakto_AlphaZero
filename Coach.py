from collections import deque
from Arena import Arena
from MCTS import MCTS
import numpy as np
from pytorch_classification.utils import Bar, AverageMeter
import time, os, sys
from pickle import Pickler, Unpickler
from random import shuffle
import tictactoe.TicTacToeLogic as logic
from tictactoe.TicTacToeGame import display
from copy import deepcopy


class Coach():
    """
    This class executes the self-play + learning. It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """
    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.pnet = self.nnet.__class__(self.game)  # the competitor network
        self.args = args
        self.mcts = MCTS(self.game, self.nnet, self.args)
        self.trainExamplesHistory = []    # history of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False # can be overriden in loadTrainExamples()
        self.boards_array = logic.Read_states_from_file(self.args.states_file)


    def executeEpisode(self,aboard=None):
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.

        Returns:
            trainExamples: a list of examples of the form (canonicalBoard,pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually won the game, else -1.
        """
        trainExamples = []

        if aboard is None:
            board = self.game.getInitBoard()
        else:
            #print 'aboard', aboard.pieces
            board = deepcopy(aboard)
            #print 'board',board.pieces
            board = board.Randomly_remove(self.args.remove_depth)

            #print board

        self.curPlayer = 1
        episodeStep = 0

        while True:
            #print(type(board))
            episodeStep += 1
            canonicalBoard = self.game.getCanonicalForm(board,self.curPlayer)
            temp = int(episodeStep < self.args.tempThreshold)
            #print temp

            pi = self.mcts.getActionProb(canonicalBoard, temp=temp)
            sym = self.game.getSymmetries(canonicalBoard.pieces, pi)
            for b,p in sym:
                trainExamples.append([b, self.curPlayer, p, None])

            action = np.random.choice(len(pi), p=pi)
            # print 'pi', pi
            # print 'action',action
            board, self.curPlayer = self.game.getNextState(board, self.curPlayer, action)

            r = self.game.getGameEnded(board, self.curPlayer)
            if r!=0:
                #print 'Endgame', board
                return [(x[0],x[2],r*((-1)**(x[1]!=self.curPlayer))) for x in trainExamples]



    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, self.args.numIters+1):
            self.train(i)
        print "--------STARTING LEAF BASED SEARCH--------"
        if self.args.leaf_based_sampling:
            for s in self.boards_array:
                display(s)
                leaf_start_point = self.args.numIters+self.boards_array.index(s)+1
                leaf_end_point = self.args.numIters+self.boards_array.index(s)+self.args.random_iterations+1
                for r in range(leaf_start_point,leaf_end_point):
                    print('------ITER FOR LEAF SAMPLING ' + str(r) + '------')
                    self.train(r,s)


    def train(self,iteration=None,board=None):

        # bookkeeping
        print('------ITER ' + str(iteration) + '------')
        # examples of the iteration
        if not self.skipFirstSelfPlay or iteration>1:
            iterationTrainExamples = deque([], maxlen=self.args.maxlenOfQueue)

            eps_time = AverageMeter()
            bar = Bar('Self Play', max=self.args.numEps)
            end = time.time()
            #for clif_state in self.board
            for eps in range(self.args.numEps):
                self.mcts = MCTS(self.game, self.nnet, self.args)   # reset search tree
                iterationTrainExamples += self.executeEpisode(board)
                #print iterationTrainExamples[0]

                # bookkeeping + plot progress
                eps_time.update(time.time() - end)
                end = time.time()
                bar.suffix  = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps+1, maxeps=self.args.numEps, et=eps_time.avg,
                                                                                                           total=bar.elapsed_td, eta=bar.eta_td)
                bar.next()
            bar.finish()

            # save the iteration examples to the history 
            self.trainExamplesHistory.append(iterationTrainExamples)
            
        if len(self.trainExamplesHistory) > self.args.numItersForTrainExamplesHistory:
            print("len(trainExamplesHistory) =", len(self.trainExamplesHistory), " => remove the oldest trainExamples")
            self.trainExamplesHistory.pop(0)
        # backup history to a file
        # NB! the examples were collected using the model from the previous iteration, so (i-1)  
        self.saveTrainExamples(iteration-1)
        
        # shuffle examlpes before training
        trainExamples = []
        for e in self.trainExamplesHistory:
            trainExamples.extend(e)
        shuffle(trainExamples)

        # training new network, keeping a copy of the old one
        self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
        self.pnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
        pmcts = MCTS(self.game, self.pnet, self.args)
        
        self.nnet.train(trainExamples)
        nmcts = MCTS(self.game, self.nnet, self.args)

        print('PITTING AGAINST PREVIOUS VERSION')
        arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                      lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), self.game)
        pwins, nwins, draws = arena.playGames(self.args.arenaCompare)

        print('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
        if pwins+nwins > 0 and float(nwins)/(pwins+nwins) < self.args.updateThreshold:
            print('REJECTING NEW MODEL')
            self.nnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
        else:
            print('ACCEPTING NEW MODEL')
            self.nnet.save_checkpoint(folder=self.args.checkpoint, filename=self.getCheckpointFile(iteration))
            self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='best.pth.tar')                


    def getCheckpointFile(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, iteration):
        folder = self.args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration)+".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed

    def loadTrainExamples(self):
        modelFile = os.path.join(self.args.load_folder_file[0], self.args.load_folder_file[1])
        examplesFile = modelFile+".examples"
        if not os.path.isfile(examplesFile):
            print(examplesFile)
            r = input("File with trainExamples not found. Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            print("File with trainExamples found. Read it.")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            f.closed
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True 
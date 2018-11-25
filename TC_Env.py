from gym import spaces
import numpy as np
import random

# class TicTacToe():

#     def __init__(self):
        
#         self.state = np.zeros((3,3))
                
#         self.all_possible_numbers =[1, 3, 5, 7, 9]

#         self.reset()


#     def is_winning(self):
#         """Takes state as an input and returns whether any row, column or diagonal has winning sum"""
#         lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
#         for line in lines:
#             line_state = self.state[line[0]] + self.state[line[1]] + self.state[line[2]]
#             if line_state == 15:
#                 return true
#         return false

#     def is_terminal(self, curr_state):
#         """Takes state as an input and returns whether it is win/tie state"""


#     def allowed_positions(self, curr_state):
#         """Takes state as an input and returns all indexes that are blank"""


#     def allowed_values(self, curr_state):
#         """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

#     def action_space(self, curr_state):
#         """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""


#     def initial_step(self, curr_state):
#         """This functions will be used only if environment is playing with the odd numbers, i.e., the environment has to make first move"""


#     def state_transition(self, curr_state, curr_action):
#         """Takes current state and action and returns the board position just after agent's move."""


#     def step(self, curr_state, curr_action):
#         """Takes current state and action and returns the next state and reward. Hint: First, check the board position after
#         agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status."""


#     def reset(self):
#         return self.state


class TicTacToe:
    def __init__(self):
        # Our 3*3 board is represented an an one dimensional array or 9 values
        # Array index is mapped as below
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.board = [0]*9
        
        #Instead of hardcoding the possible values, the env will be able to handle 2 set of players 
        # Odd player has only options [1, 3, 5, 7, 9]
        self.player1 = None # These values are passed as input to the QLearning process
        # Even player has only options [2, 4, 6, 8]
        self.player2 = None # These values are passed as input to the QLearning process

    #reset the game
    def reset(self):
        self.board = [0] * 9

   #evaluate function
    def evaluate(self):
        # "rows checking"
        # 0->1->2 = 15
        # 3->4->5 = 15
        # 6->7->8 = 15
        for i in range(3):
            if (self.board[i * 3] + self.board[i * 3 + 1] + self.board[i * 3 + 2]) == 15:
                return 1.0, True
        
        # "col checking"
        for i in range(3):
            if (self.board[i + 0] + self.board[i + 3] + self.board[i + 6]) == 15:
                return 1.0, True
        
        # diagonal checking
        if (self.board[0] + self.board[4] + self.board[8]) == 15:
            return 1.0, True
        if (self.board[2] + self.board[4] + self.board[6]) == 15:
            return 1.0, True

        # "if filled draw"
        if not any(space == 0 for space in self.board):
            return 0.0, True

        return 0.0, False

    #return remaining possible moves
    def possibleMoves(self):
        blank_spots =  [moves + 1 for moves, spot in enumerate(self.board) if spot == 0]
        return blank_spots

    #pick a possible move based on the odd or even player
    def pickMove(self, isX):
        # we will shuffle the set of remaining options and pop the first from the list to be used for our move.
        if(isX):
            self.player1.options = random.sample(self.player1.options, len(self.player1.options))
            return self.player1.options.pop()
        # in our setup we have one set of player playing odd and the other even, 
        # so we need to switch between the two to determine the next move pick
        else:
            self.player2.options = random.sample(self.player2.options, len(self.player2.options))
            return self.player2.options.pop()

    #take next step and return reward
    def step(self, isX, move):
        self.board[move-1]= self.pickMove(isX)
        reward, done = self.evaluate()
        return reward, done

    #begin training
    def startTraining(self, player1, player2, iterations, odd=True, verbose = False):
        self.player1=player1
        self.player2=player2
        print ("Training Started")
        for i in range(iterations):
            if verbose: print("trainining ", i)
            self.player1.game_begin()
            self.player2.game_begin()
            self.reset()
            done = False

            # Note that the odd player always begins the game for our simulation and is set to true by default
            isX = odd
            while not done:
                if isX:
                    move = self.player1.epslion_greedy(self.board, self.possibleMoves())
                else:
                    move = self.player2.epslion_greedy(self.board, self.possibleMoves())

                reward, done = self.step(isX, move)

                if (reward == 1):  # won
                    if (isX):
                        self.player1.updateQ(10, self.board, self.possibleMoves())
                        self.player2.updateQ(-10, self.board, self.possibleMoves())
                    else:
                        self.player1.updateQ(-10, self.board, self.possibleMoves())
                        self.player2.updateQ(10, self.board, self.possibleMoves())

                else: #(reward == 0):  draw
                    self.player1.updateQ(reward, self.board, self.possibleMoves())
                    self.player2.updateQ(reward, self.board, self.possibleMoves())


                isX = not isX  # switch players
        print ("Training Complete")

    #save Qtables
    def saveStates(self):
        self.player1.saveQ("oddPolicy")
        self.player2.saveQ("evenPolicy")

    #return Qtables
    def getQ(self):
        return self.player1.Q, self.player2.Q



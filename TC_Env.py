from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        
        self.state =
        self.all_possible_numbers =

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum"""

    def is_terminal(self, curr_state):
        """Takes state as an input and returns whether it is win/tie state"""


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""


    def initial_step(self, curr_state):
        """This functions will be used only if environment is playing with the odd numbers, i.e., the environment has to make first move"""


    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move."""


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state and reward. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status."""


    def reset(self):
        return self.state

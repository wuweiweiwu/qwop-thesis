import pyautogui as control
import random
import time
import string
from game_detector import GameDetector

class QWOPEnv:

    def __init__(self):
        self.game = GameDetector()
        # get dimensions of np array
        self.observation_space = self.game.get_state().shape[0]
        # 16 possible combinations
        self.action_space = 16
        self.prev_score = None

    def reset(self):
        # returns initial state
        self.game.new_game()
        self.prev_score = None
        return self.game.get_state()

    # def render(self):
    #     continue

    # do this step
    def step(self, action):
        # action is number between 0 - 15
        # returns next_state, reward, done`
        letter = string.lowercase[action]
        print 'action: ', letter

        self.game.eval(letter)
        next_state = self.game.get_state()
        new_score = self.game.get_score()
        print 'new score: ', new_score
        reward = new_score if not self.prev_score else new_score - self.prev_score
        done = self.game.is_end()
        self.prev_score = new_score
        return next_state, reward, done, letter

if __name__ == '__main__':
    env = QWOPEnv()
    env.reset()
    for i in range(16):
        print env.step(i)

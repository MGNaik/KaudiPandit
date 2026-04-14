from enum import Enum
import random

class KaudiState(Enum):
    UP = 'up'
    DOWN = 'down'
    NOT_ROLLED = 'not_rolled'


class Kaudi:
    def __init__(self, up_prob=0.5):
        self.state = KaudiState.NOT_ROLLED
        self.up_prob = up_prob
    
    def roll(self):
        self.state = random.choices([KaudiState.UP, KaudiState.DOWN], weights=[self.up_prob, 1-self.up_prob])[0]
    
    def reset(self):
        self.state = KaudiState.NOT_ROLLED

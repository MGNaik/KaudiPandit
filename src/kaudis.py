from enum import Enum
import random

class KaudiState(Enum):
    UP = 'up' # Up is the mouth of the kaudi up, open side, flat side - which counts as 1
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


class KaudiSet:
    def __init__(self, num_kaudis=6, up_prob_list=None):
        if up_prob_list is None:
            up_prob_list = [0.5 for i in range(num_kaudis)]
        self.kaudis = [Kaudi(up_prob=up_prob_list[i]) for i in range(num_kaudis)]
        self.KaudiSetValue = 0
        
    def roll(self):
        self.KaudiSetValue = 0
        for kaudi in self.kaudis:
            kaudi.roll()
            if (kaudi.state == KaudiState.UP):
                self.KaudiSetValue += 1
        if self.KaudiSetValue == 0:
            self.KaudiSetValue = 12
        for kaudi in self.kaudis:
            kaudi.reset()





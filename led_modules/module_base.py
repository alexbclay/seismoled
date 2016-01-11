#!/usr/bin/env python
import random

class LedActionModule:
    def __init__(self, length):
        self.length = length
        # any other self vars?
        pass

    def trigger(self):
        ''' Something happened, return a list of colors to write to the leds'''
        pass

    def time_step(self):
        ''' Nothing happened, return a list of colors to write to the leds
        or None if keeping the same colors '''
        return None

    def random_color(self, weight=(1,1,1), min=(0,0,0)):
        '''
        Random color with weight(0,1)
           and minimum color (0,255)
        '''
        return tuple(int(min[i] +
                         (random.random() *
                          weight[i] *
                          (255 - min[i])))
                     for i in range(3))

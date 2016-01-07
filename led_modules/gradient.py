#!/usr/bin/env python
from module_base import LedActionModule
import random

class Gradient(LedActionModule):
    def __init__(self, length, color_start=None, color_end=None):
        ''' Set the colors for the gradient '''
#        import pdb; pdb.set_trace()
#        super(Gradient, self).__init__(length)

        if color_start:
            self.color_start = color_start
        else:
            self.color_start = self.random_color()

        if color_end:
            self.color_end = color_end
        else:
            self.color_end = self.random_color()

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

    def trigger(self):
        return self.make_gradient

    def make_gradient(self, length=None, color_start=[], color_end=[]):
        if not length:
            length = self.length
        diff = map(lambda x,y: (y - x) / (float(length) - 1), color_start, color_end)
        result = []
        for i in range(length):
            result.append(map(lambda x,y: int(ceil(x + y * i)), color_start, diff))
        return result

#!/usr/bin/env python
from module_base import LedActionModule
from math import ceil, floor


class Gradient(LedActionModule):
    def __init__(self, length, color_start=None, color_end=None):
        ''' Set the colors for the gradient '''
        #        import pdb; pdb.set_trace()
        #        super(Gradient, self).__init__(length)

        self.length = length
        if color_start:
            self.color_start = color_start
        else:
            self.color_start = self.random_color()

        if color_end:
            self.color_end = color_end
        else:
            self.color_end = self.random_color()

    def time_step(self):
        self.color_start = self.random_color()
        self.color_end = self.random_color()
        return self.make_gradient()

    def trigger(self):
        return self.make_gradient()

    def make_gradient(self, length=None, color_start=None, color_end=None):

        if not length:
            length = self.length
        if not color_start:
            color_start = self.color_start
        if not color_end:
            color_end = self.color_end

        diff = map(lambda x,y: (y - x) / (float(length) - 1), color_start, color_end)
        result = []
        for i in range(length):
            result.append(tuple(map(lambda x,y: int(ceil(x + y * i)), color_start, diff)))
        return result

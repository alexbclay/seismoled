#!/usr/bin/env python
from module_base import LedActionModule
import random
from datetime import datetime

class BinaryClock(LedActionModule):
    def __init__(self, length, bg_color=None, digit_color=None, separate_color=None):
        self.length = length
        self.bg_color = bg_color or self.random_color()
        self.separate_color = separate_color or self.random_color()

        self.binary_colors = [self.bg_color,
                              digit_color or self.random_color()]

    def time_step(self):
        ''' make a clock! '''
        now = datetime.now().timetuple()

        ret = [self.separate_color]

        ret.extend(self.to_binary_array(now.tm_hour))
        ret.append(self.separate_color)
        ret.extend(self.to_binary_array(now.tm_min))
        ret.append(self.separate_color)
        ret.extend(self.to_binary_array(now.tm_sec))
        ret.append(self.separate_color)

        return ret

    def trigger(self):
        return self.time_step()

    def to_binary_array(self, number):
        ''' convert a number into an array of its binary representation '''
        return map(lambda b: self.binary_colors[int(b)], "{0:06b}".format(number))

#!/usr/bin/env python
from module_base import LedActionModule
import random
from datetime import datetime

class BinaryClock(LedActionModule):
    def __init__(self, length, bg_color=None, digit_color=None, separate_color=None):
        self.length = length
        self.bg_color = bg_color or (128,128,128)
        self.separate_color = separate_color or (10,10,255)

        self.binary_colors = [self.bg_color,
                              digit_color or (255,10,10)]

    def time_step(self):
        ''' make a clock! '''
        now = datetime.now().timetuple()

        ret = [self.separate_color]

        ret.extend(self.to_binary_array(now.tm_hour))
        ret.append(self.separate_color)
        ret.extend(self.to_binary_array(now.tm_min))
        ret.append(self.separate_color)
        ret.extend(self.to_binary_array(now.tm_sec))

        return ret

    def trigger(self):
        return self.time_step()

    def to_binary_array(self, number):
        ''' convert a number into an array of its binary representation '''
        return map(lambda b: self.binary_colors[int(b)], "{0:06b}".format(number))

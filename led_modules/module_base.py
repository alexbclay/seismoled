#!/usr/bin/env python

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

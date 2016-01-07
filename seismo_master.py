#!/usr/bin/env python
from Adafruit_BBIO import SPI, GPIO
from math import ceil, floor
import random
import time

# Get a colors library so we don't need to do so much RGB arrays?

class LedBase:
    def __init__(self, length, base_color):
        ''' init the interface '''
        self.length = length
        self.base_color = base_color

    # funcs
    def write(self, index, color):
        ''' Write one color in one place '''
        pass

    def write_all(self, color_array, from=0, to=None):
        ''' Write a list of colors '''
        pass

    def reset(self):
        ''' Reset all colors to default '''
        pass

    

class SeismoEngine (LedBase):
    def __init__(self, length, iface_addr=(0,1), default_background=(0,0,0)):
        self.background = default_background
        self.interface = SPI.SPI(*iface_addr)
        self.length = length

    def write(self, data=None):
        # clear bytes
        self.interface.writebytes([0,0,0]*(self.length/32+1))
        if data:
            self.interface.writebytes(data)
        else:
            for value in self.buffer:
                self.interface.writebytes(value)
            #self.interface.writebytes([128,128,128])

    def clear(self):
        self.buffer = [self.background] * self.length
        self.write()

    def make_gradient(self, length=None, color_start=[], color_end=[]):
        if not length:
            length = self.length
        diff = map(lambda x,y: (y - x) / (float(length) - 1), color_start, color_end)
        result = []
        for i in range(length):
            result.append(map(lambda x,y: int(ceil(x + y * i)), color_start, diff))
        return result

    def gradient(self, length=None, color_start=[], color_end=[]):
        if not length:
            length = self.length
        self.buffer = self.make_gradient(length, color_start, color_end)
        self.write()

    def moving_gradient(self, length=None, colors=[], timestep=0.1, shiftsteps=20):
        if not length:
            length = self.length
        self.gradient(length, colors[0], colors[1])
        time.sleep(timestep)
        for i in range(2, len(colors), 2):
            start_gradient = self.make_gradient(shiftsteps, colors[i-2], colors[i])
            for value in start_gradient:
                self.gradient(length, value, colors[i-1])
                time.sleep(timestep)
            end_gradient = self.make_gradient(shiftsteps, colors[i-1], colors[i+1])
            for value in end_gradient:
                self.gradient(length, colors[i], value)
                time.sleep(timestep)

    def whole_moving_gradient(self, length=None, colors=[], timestep=0.1, shiftsteps=20):
        if not length:
            length = self.length
        for i in range(0, len(colors), 2):
            grad = self.make_gradient(shiftsteps, colors[i], colors[i + 1])
            for index in range(0, shiftsteps):
                self.buffer = [grad[index]] * length
                self.write()
                time.sleep(timestep)

    def whole_pattern_shift(self, pattern, timestep=0.1, shiftsteps=20):
	final_gradient = []
	gradient_steps = []
	for i in range(0, len(self.buffer)):
	    gradient_steps += [self.make_gradient(length=shiftsteps, color_start=self.buffer[i], color_end=pattern[i])]
	for i in range(0, shiftsteps):
	    self.buffer = []
	    for j in range(0, len(gradient_steps)):
		self.buffer += [gradient_steps[j][i]]
	    self.write()
	    time.sleep(timestep)

    def set_slow_clear(self, shiftsteps=20):
	gradient_steps = []
	self.slow_clear_gradient = []
	for i in range(0, len(self.buffer)):
	    gradient_steps += [self.make_gradient(length=shiftsteps, color_start=self.buffer[i], color_end=self.background)]
	for i in range(0, shiftsteps):
	    subgrad = []
	    for j in range(0, len(gradient_steps)):
		subgrad +=[gradient_steps[j][i]]
	    self.slow_clear_gradient += [subgrad]
	

    def cancel_slow_clear(self):
	self.slow_clear_gradient = None

    def slow_clear(self):
	if self.slow_clear_gradient:
	    self.buffer = self.slow_clear_gradient.pop(0)#] * self.length
	    self.write()
	    if not self.slow_clear_gradient:
	    	return True
	#else:
	#    self.buffer = []



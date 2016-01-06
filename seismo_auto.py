#!/usr/bin/env python
from Adafruit_BBIO import SPI, GPIO
from math import ceil, floor
import random
import time

class SpiLedStrip:
    def __init__(self, length, iface_addr=(0,1), background=[0,0,0]):
        self.background = background #[background[i] + 128 for i in background]
        self.interface = SPI.SPI(*iface_addr)
        self.length = length
	self.slow_clear_gradient = None

    def write(self, data=None):
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
	

class GroveLedStrip(SpiLedStrip):
    def __init__(self, length=24, iface_addr=(0,0), background=[0,0,0]):
        SpiLedStrip.__init__(self, length, iface_addr, background)
        self.interface.msh = 100000 #max clock
        self.interface.mode = 0
        self.clear()

    def write(self, data=None):
        self.interface.writebytes([0] * 4)
        if data:
            self.interface.writebytes(data)
        else:
            for value in self.buffer:
                chk = sum([((value[i] & 192) ^ 192) >> ((i + 1) * 2) for i in range(0, len(value))]) + 192
                self.interface.writebytes([chk] + value)
	self.interface.writebytes([0] * 4)
            

def random_color(weight=[0.6, 0.6, 1.0], min=[0,0,0]):
    return [int(min[i] + random.random() * weight[i] * (255 - min[i])) for i in range(3)]


sensor_pin = "P8_26"

led = GroveLedStrip(24, background=[0x00, 0x08, 0x70])
GPIO.setup(sensor_pin, GPIO.IN)
"""grad = [[0,0,0], [0,0,0],
        random_color(), random_color()]"""
grad = [led.background, random_color()]
timeout = 0

led_patterns = [[[0x00,0x10,0xee],#00
                 [0x10,0x00,0x00],#01
                 [0x10,0x00,0x00],#02
                 [0x10,0x00,0x00],#03
                 [0x10,0x00,0x00],#04
                 [0x10,0x00,0x00],#05
                 [0x10,0x00,0x00],#06
                 [0x10,0x00,0x00],#07
                 [0x10,0x00,0x00],#08
                 [0x10,0x00,0x00],#09
                 [0x10,0x00,0x00],#10
                 [0x10,0x00,0x00],#11
                 [0x10,0x00,0x00],#12
                 [0x10,0x00,0x00],#13
                 [0x10,0x00,0x00],#14
                 [0x10,0x00,0x00],#15
                 [0x10,0x00,0x00],#16
                 [0x10,0x00,0x00],#17
                 [0x10,0x00,0x00],#18
                 [0x10,0x00,0x00],#19
                 [0x10,0x00,0x00],#20
                 [0x10,0x00,0x00],#21
                 [0x10,0x00,0x00],#22
                 [0x00,0x10,0xee],#23
                 [0x00,0x10,0xee],],
                [[0xee,0x10,0x00],#00
                 [0x00,0x10,0x00],#01
                 [0x00,0x10,0x00],#02
                 [0x00,0x10,0x00],#03
                 [0x00,0x10,0x00],#04
                 [0x00,0x10,0x00],#05
                 [0x00,0x10,0x00],#06
                 [0x00,0x10,0x00],#07
                 [0x00,0x10,0x00],#08
                 [0x00,0x10,0x00],#09
                 [0x00,0x10,0x00],#10
                 [0x00,0x10,0x00],#11
                 [0x00,0x10,0x00],#12
                 [0x00,0x10,0x00],#13
                 [0x00,0x10,0x00],#14
                 [0x00,0x10,0x00],#15
                 [0x00,0x10,0x00],#16
                 [0x00,0x10,0x00],#17
                 [0x00,0x00,0x00],#18
                 [0x00,0x00,0x00],#19
                 [0x00,0x00,0x00],#20
                 [0x00,0x00,0x00],#21
                 [0xee,0x10,0x00],#22
                 [0xee,0x10,0x00],#23
                 [0xee,0x10,0x00],],
                [[0xee,0x00,0x10],#00
                 [0x00,0x00,0x10],#01
                 [0x00,0x00,0x10],#02
                 [0x00,0x00,0x10],#03
                 [0x00,0x00,0x10],#04
                 [0x00,0x00,0x10],#05
                 [0x00,0x00,0x10],#06
                 [0x00,0x00,0x10],#07
                 [0x00,0x00,0x10],#08
                 [0x00,0x00,0x10],#09
                 [0x00,0x00,0x10],#10
                 [0x00,0x00,0x10],#11
                 [0x00,0x00,0x10],#12
                 [0x00,0x00,0x10],#13
                 [0x00,0x00,0x10],#14
                 [0x00,0x00,0x10],#15
                 [0x00,0x00,0x10],#16
                 [0x00,0x00,0x10],#17
                 [0x00,0x00,0x10],#18
                 [0x00,0x00,0x10],#19
                 [0x00,0x00,0x10],#20
                 [0x10,0x00,0x10],#21
                 [0x10,0x00,0x10],#22
                 [0x00,0x80,0x10],#23
                 [0xee,0x00,0x10],],
                [[0xee,0x00,0x10],#00
                 [0x00,0x00,0x10],#01
                 [0x00,0x00,0x10],#02
                 [0x00,0x00,0x10],#03
                 [0x00,0x00,0x10],#04
                 [0x00,0x00,0x10],#05
                 [0x00,0x00,0x10],#06
                 [0x00,0x00,0x10],#07
                 [0x00,0x00,0x10],#08
                 [0x00,0x00,0x10],#09
                 [0x00,0x00,0x10],#10
                 [0x00,0x00,0x10],#11
                 [0x00,0x00,0x10],#12
                 [0x00,0x00,0x10],#13
                 [0x00,0x00,0x10],#14
                 [0x00,0x00,0x10],#15
                 [0x00,0x00,0x10],#16
                 [0x00,0x00,0x10],#17
                 [0x00,0x00,0x10],#18
                 [0x00,0x00,0x10],#19
                 [0x00,0x00,0x10],#20
                 [0x10,0x00,0x10],#21
                 [0x10,0x00,0x10],#22
                 [0x00,0x80,0x10],#23
                 [0xee,0x00,0x10],],
		'moving_gradient',
		'ripple',
            ]

pattern_selection = None

while True:
    if not GPIO.input(sensor_pin):	
	timeout = 0
	led.cancel_slow_clear()
	if not pattern_selection:
	    #pattern_selection = led_patterns[int(floor(random.random() * len(led_patterns)))]
	    pattern_selection = ['moving_gradient', 'ripple'][int(floor(random.random() * 2))]
	    if pattern_selection == 'moving_gradient':
		grad = [led.background, led.background]
	    elif pattern_selection == 'ripple':
		color = random_color() #[0,32,255]
		#bgcolor = [0,0,0]
		#pattern_selection = [ripple[2], ripple[1], ripple[0]] + [[0,0,0]] * 22
	    else:
		pattern_selection = list(pattern_selection)
	if pattern_selection == 'moving_gradient':
	    date = time.localtime()
	    if date.tm_mday == 11 and date.tm_mon == 6:
		grad = grad[1:] + [random_color(weight=[0, 0.2, 1.0], min=[0, 0, 150])]
	    else:
		grad = grad[1:] + [random_color()]
	    led.whole_moving_gradient(colors=grad, timestep=0.06, shiftsteps=12)
	elif pattern_selection == 'ripple':
	    ripple = [[int(i * .1) for i in color], [int(i * .2) for i in color], [int(i * .4) for i in color], [int(i * .75) for i in color], [int(i * .9) for i in color], color]
	    for i in range(24 + len(ripple)):
		if i < len(ripple):
			led.buffer = ripple[-i-1:] + [led.background] * (25 - i)
		else:
			led.buffer = ([led.background] * (i - len(ripple) + 1)) + ripple + ([led.background] * ((25 - i)))
		led.write()
		time.sleep(0.05)
	else:
	    print len(pattern_selection)
	    led.whole_pattern_shift(pattern=pattern_selection, timestep=0.06, shiftsteps=4)
	    pattern_selection = [pattern_selection.pop(-1)] + pattern_selection
	    print "end of loop"
	time.sleep(0.25)
    else:
	if timeout >= 60:
	    led.set_slow_clear(shiftsteps=24)
	    led.slow_clear()
	    timeout = 0
	else:
	    timeout += 1
	    if led.slow_clear():
		pattern_selection = None
	    time.sleep(0.05)

#!/usr/bin/env python
'''
import led_modules
from pprint import pprint

if __name__ == '__main__':
    gradient = led_modules.gradient.Gradient(10)
    print gradient.random_color(weight=(0,0.5,1),min=(128,128,255))
'''

import Tkinter as tk
import random
import led_modules

class App(tk.Frame):
    num_leds = 24
    module = led_modules.gradient.Gradient(num_leds)
    def __init__(self, master=None, len=24):
        tk.Frame.__init__(self, master)

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # make a canvas to draw on
        self.led_canvas = tk.Canvas(self, width=100, height=24*40)
        self.led_canvas.grid()

        self.step()

        # button for steps
        self.stepButton = tk.Button(self, text='Step', command=self.step)
        self.stepButton.grid()

        # button to quit~
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

    def setup(length, module):
        self.num_leds=24
        self.module = module

    def do_time_step(self):
        self.draw_array(self.module.time_step())
        self.after(200, self.do_time_step)

    def draw_array(self, array):
        if not array:
            return
        for i in range(min(24,len(array))):
            self.led_canvas.create_rectangle(6,5 + 40*i+1, 98, 40*(i+1)-1, fill='#%02x%02x%02x' % array[i])
        for i in range(self.num_leds):
            self.led_canvas.create_rectangle(5,5 + 40*i, 99, 40*(i+1),)
        print array

    def step(self):
        self.draw_array(self.module.trigger())
        '''
        start_color = tuple(random.random() * 255 for i in range(3))
        inc_color = tuple(random.random() * 25 for i in range(3))

        print start_color
        print inc_color
        self.draw_array([tuple((start_color[i] + (inc_color[i] * led)) % 255 for i in range(3)) for led in range(self.num_leds)])
        '''

app = App()

app.master.title('Stairs Simulator!')
app.after(200,app.do_time_step)
app.mainloop()

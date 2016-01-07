#!/usr/bin/env python
'''
import led_modules
from pprint import pprint

if __name__ == '__main__':
    gradient = led_modules.gradient.Gradient(10)
    print gradient.random_color(weight=(0,0.5,1),min=(128,128,255))
'''

import Tkinter as tk


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        def make_fun(i):
            def p ():
                print "button {}".format(i)
            return p

        for i in range(10):
            b = tk.Button(self, text='Button {}'.format(i), command=make_fun(i))
            b.grid()

        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

app = App()

app.master.title('Sample')
app.mainloop()

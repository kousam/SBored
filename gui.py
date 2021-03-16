from tkinter import *
import tkinter.font as font
from tkinter import ttk

import time
import threading



class SB_Button(ttk.Button):
    def __init__(self, parent, title, play_cmd, stop_cmd):
        ttk.Button.__init__(self, parent)

        self.title = title

        self['text'] = title
        self['width'] = 12

        self.play_cmd = play_cmd
        self.stop_cmd = stop_cmd
        
        self['command'] = self.play_action
        self['style'] = 'off.TButton'

        self.interupt = False

        self.duration = 0
        
    def play_action(self):
        self.duration = self.play_cmd(self.title)

        self['command'] = self.stop_action
        self['style'] = 'on.TButton'

        self.interupt = False

        t = threading.Thread(target=self.sleep)
        t.start()
        

    def stop_action(self):
        self.stop_cmd()
        self.interupt = True

    def sleep(self):
        past_time = 0
        while not self.interupt:
            past_time += 0.1
            time.sleep(0.1)

            if past_time >= self.duration:
                self.interupt = True
        
        self['command'] = self.play_action
        self['style'] = 'off.TButton'
    


class GUI:
    def __init__(self, _app):
        self.app = _app
        
        self.root = Tk()
        self.root.title('SoundBoard')

        s = ttk.Style()
        s.configure('off.TButton', font=('Consolas', 12))
        s.configure('on.TButton', font=('Consolas', 12), background = 'green')

        self.w_init = 616
        self.h_init = 490
        self.w = self.w_init
        self.h = self.h_init
        self.x_init = 600
        self.y_init = 400
        self.rect = '{}x{}+{}+{}'.format(self.w, self.h, self.x_init, self.y_init)
        self.root.geometry(self.rect)
        self.root.resizable(width = False, height = False)

        self.main_frame = ttk.Frame(self.root)
        #self.main_frame.grid({'row':0, 'column':0, 'sticky':'nsew'})
        self.main_frame.pack({'anchor': 'w', 'padx': 10, 'pady': 5})

        self.grid_x = 0
        self.grid_y = 0


        self.loadButtons()

            
        
        

    def newButton(self, title):
        
        b = SB_Button(self.main_frame, title, self.app.play, self.app.stop)
        
        
        b.grid({'row':self.grid_x, 'column':self.grid_y, 'sticky':'nsew','padx': 5, 'pady': 5, 'ipadx': 10, 'ipady': 40})

        self.grid_y += 1

        if self.grid_y >= 4:
            self.grid_x += 1
            self.grid_y = 0

    def loadButtons(self):
        titles = self.app.getTitles()
        for title in titles:
            self.newButton(title)
            
            

    

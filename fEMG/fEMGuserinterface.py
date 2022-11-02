#!/usr/bin/env python
# coding: utf-8

# In[1]:
#combined
import serial
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
style.use('ggplot')

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
time.sleep(2)
data = arduino.readline()
size = 10
x_vec = np.ones(size)
y_vec = np.ones(size)
ZMrelax = 0 #peak corresponding with relaxed ZM
ZMcontract = 2000 #peak corresponding with contracted ZM
CSrelax = 0 #peak corresponding with relaxed CS
CSraised = 2000 #peak corresponding with contracted CS

fig = Figure(figsize=(13, 6))
ax = fig.add_subplot(111)

def read():
    data = arduino.readline()
    if data:
        data_decoded = data.decode()
        num_list = data_decoded.strip().split()
        eyebrow = int(num_list[0])
        cheek = int(num_list[1])
    return eyebrow, cheek

def calibration(labels):
    #ZM relax and CS relax
    global ZMrelax, ZMcontract, CSrelax, CSraised
    ZM = np.zeros(10)
    CS = np.zeros(10)
    messagebox.showinfo('Calibration', 'Maintain a relaxed, neutral expression')
    for i in range(0,10):
        eyebrow, cheek = read()
        CS[i] = eyebrow
        ZM[i] = cheek
        time.sleep(0.2)
    ZMrelax = np.median(ZM)
    CSrelax = np.median(CS)
    labels[0].config(text="ZM Relax Value:" + str(ZMrelax))
    labels[1].config(text="CS Relax Value:" + str(CSrelax))
    messagebox.showinfo('Calibration', 'Relax Calibration Done')
    
    messagebox.showinfo('Calibration', 'Now give a big smile!')
    #ZM contract
    for i in range(0,10):
        eyebrow, cheek = read()
        ZM[i] = cheek
        time.sleep(0.2)
    ZMcontract = np.median(ZM)
    labels[2].config(text="ZM Contract Value:" + str(ZMcontract))
    messagebox.showinfo('Calibration', 'ZM Calibration Done')
    
    messagebox.showinfo('Calibration', 'Now raise your eyebrows, nice and high!')
    #CS raised
    for i in range(0,10):
        eyebrow, cheek = read()
        CS[i] = cheek
        time.sleep(0.2)
    CSraised = np.median(CS)
    labels[3].config(text="CS Raised Value:" + str(CSraised))
    messagebox.showinfo('Calibration', 'CS Calibration Done. All complete. Thank you!')
    app.update()

#def read():
#    data = arduino.readline()
#    if data:
#        data_decoded = data.decode()
#        num_list = data_decoded.strip().split()
#        eyebrow = int(num_list[0])
#        cheek = int(num_list[1])
#    return eyebrow, cheek

def live_plotter(identifier='', pause_time=0.1):
    global x_vec, y_vec, ZMrelax, ZMcontract, CSrelax, CSraised
    eyebrow, cheek = read()
    x_vec = np.append(x_vec[1:], eyebrow)
    y_vec = np.append(y_vec[1:], cheek)
    ax.clear()
    ax.set_xlabel('Eyebrow')
    ax.set_ylabel('Cheek')
    ax.set_xlim([0, 10240])
    ax.set_ylim([0, 10240])
    ax.axvline(x=CSrelax,dashes=(5,3),label='Brow Relaxed',color='blue')
    ax.axvline(x=CSraised,dashes=(5,3),label='Brow Raised',color='black')
    ax.axhline(y=ZMrelax,dashes=(5,3),label='Cheek Relaxed',color='purple')
    ax.axhline(y=ZMcontract,dashes=(5,3),label='Cheek Contracted',color='orange')
    ax.plot(x_vec, y_vec)
    ax.legend()

# In[3]:


from tkinter import *
from tkinter.ttk import *
 
LARGEFONT =("Verdana", 35)

x_vec = np.zeros(size)
y_vec = np.zeros(size)

class tkinterApp(Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        Tk.__init__(self, *args, **kwargs)
        
        self.browclassifier = StringVar(value="Hello")
        self.cheekclassifier = StringVar()
         
        # creating a container
        container = Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, PageCalibrate):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
        self.update_labels()
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def update_labels(self):
        if sum(y_vec > (ZMcontract-ZMrelax)+ZMrelax) > 7:
            self.browclassifier.set("Brow: Contracted")
        elif sum(y_vec < (ZMcontract-ZMrelax)+ZMrelax) > 7:
            self.browclassifier.set("Brow: Relaxed")
        else:
            self.browclassifier.set("Brow: Unclear")
        if sum(x_vec > (CSraised-CSrelax)+CSrelax) > 7:
            self.cheekclassifier.set("Cheek: Raised")
        elif sum(x_vec < (CSraised-CSrelax)+CSrelax) > 7:
            self.cheekclassifier.set("Cheek: Relaxed")
        else:
            self.cheekclassifier.set("Cheek: Unclear")
        self.after(1000, self.update_labels)
        
  
# first window frame startpage
  
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = Label(self, text ="EmoTrack", font = LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        ## button to show frame 2 with text layout2
        button2 = Button(self, text ="Calibrate",
        command = lambda : controller.show_frame(PageCalibrate))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        cheeklabel = Label(self, textvariable = controller.cheekclassifier)
        cheeklabel.grid(row=1,column = 2, padx=10, pady=10)
        browlabel = Label(self, textvariable = controller.browclassifier)
        browlabel.grid(row=2,column = 2, padx=10, pady=10)
        
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
        toolbar.update()
        canvas.get_tk_widget().grid(row = 3, column = 1, padx = 10, pady = 10)
        toolbar.grid(row = 4, column = 1, padx = 10, pady = 10)
  
  
# second frame page2
class PageCalibrate(Frame):
    def __init__(self, parent, controller):
        global ZMrelax, CSrelax, ZMcontract, CSraised
        Frame.__init__(self, parent)
        label = Label(self, text ="Calibration", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
        
        ZMrelaxlabel = Label(self, text = "ZM Relax Value:" + str(ZMrelax), font = LARGEFONT)
        CSrelaxlabel = Label(self, text = "CS Relax Value:" + str(CSrelax), font = LARGEFONT)
        ZMcontractlabel = Label(self, text = "ZM Contract Value:" + str(ZMcontract), font = LARGEFONT)
        CSraisedlabel = Label(self, text = "CS Raised Value:" + str(CSraised), font = LARGEFONT)
        labels = [ZMrelaxlabel, CSrelaxlabel, ZMcontractlabel, CSraisedlabel]
        
        # button to show frame 3 with text
        # layout3
        button1 = Button(self, text ="Begin Calibration",
                            command = lambda : calibration(labels))
        button1.grid(row=1,column = 1, padx = 10, pady = 10)
  
        # button to show frame 3 with text
        # layout3
        button2 = Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
        
        ZMrelaxlabel.grid(row = 1, column = 2, padx = 10, pady = 10)
        CSrelaxlabel.grid(row = 2, column = 2, padx = 10, pady = 10)
        ZMcontractlabel.grid(row = 3, column = 2, padx = 10, pady = 10)
        CSraisedlabel.grid(row = 4, column = 2, padx = 10, pady = 10)

ani = animation.FuncAnimation(fig,live_plotter, interval=100)
# Driver Code
app = tkinterApp()
app.mainloop()

# In[4]:
arduino.close()

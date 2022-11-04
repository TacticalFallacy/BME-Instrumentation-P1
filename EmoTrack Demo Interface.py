# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 17:08:50 2022

@author: limji
"""

import serial
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.animation as animation
from matplotlib import style
import numpy as np
style.use('ggplot')

from tkinter import *
#from tkinter.ttk import *
from tkinter import messagebox
import random

import pandas as pd
import datetime

relaxcheek = 3 #corresponding with relaxed cheek
relaxbrow = 3 #corresponding with relaxed brow
restHR = 60 #resting heart-rate
maxcheek = 1 #maximum measured brow value
maxbrow = 1 #maximum measured brow value

record = []
recording = False
browbuffer = []
cheekbuffer = []
HRbuffer = []

def pause():
    global pauseplay
    if pauseplay:
        pauseplay = False
    else:
        pauseplay = True
        
def recordonoff():
    global recording
    global record
    if recording:
        recording = False
        name = datetime.datetime.now().strftime("%H-%M-%S.csv")
        df = pd.DataFrame(record, 
                          columns = ['Time','Brow', 'Cheek', 
                                     'Brow Max', 'Cheek Max', 
                                     'Brow Relax','Cheek Relax',
                                     'Valence Choice'])
        df.to_csv(name, index=False)
        record = []
        recordvar.set("Recording:OFF")
        print('Recording saved as ' + name)
    else:
        recording = True
        recordvar.set("Recording:ON")
        
def calibrate():
    global relaxcheek, relaxbrow, restHR
    cheeklist = np.zeros(20)
    browlist = np.zeros(20)
    HRlist = np.zeros(20)
    messagebox.showinfo('Calibration', 'Maintain a relaxed, neutral expression')
    for i in range(0,20):
        eyebrow, cheek, HR = read()
        browlist[i] = eyebrow
        cheeklist[i] = cheek
        HRlist[i] = HR
        time.sleep(0.2)
    relaxcheek = np.median(cheeklist)
    relaxbrow = np.median(browlist)
    restHR = np.median(HRlist)
    messagebox.showinfo('Calibration', 'Calibration Complete')
    
def HRmodechange():
    global HRmode
    global HRlabelvar
    if HRmode:
        HRmode = False
        HRlabelvar.set('HR Integration: OFF')
    else:
        HRmode = True
        HRlabelvar.set('HR Integration: ON')
        
# read eyebrow and cheek data
def read():
    global HRmode
    fEMG.reset_input_buffer()
    heartrate.reset_input_buffer()
    data = fEMG.readline()
    HR = heartrate.readline()
    if HRmode:
        if HR:
            data_decoded = HR.decode()
            num_list = data_decoded.strip().split()
            HRreading = int(num_list[0])
        else:
            HRreading = 0
    else:
        if HR:
            HRreading = 1
        else:
            HRreading = 0
    if data:
        data_decoded = data.decode()
        num_list = data_decoded.strip().split()
        eyebrow = int(num_list[0])
        cheek = int(num_list[1])
    else:
        eyebrow = 0
        cheek = 0
    return eyebrow, cheek, HRreading

#function that classifies positive or negative based on relative values
def classify(eyebrow, cheek, HRreading):
    global record
    if HRmode:
        HRmultiplier = HRreading/restHR
        HRvar.set(str(round(HRreading)))
    else:
        HRmultiplier = 1
        if HRreading == 1:
            HRvar.set('Heart Rate Detected. \n Turn on HR Mode to integrate.')
        else:   
            HRvar.set('')
    classifier = ((cheek*HRmultiplier)/maxcheek - (eyebrow*HRmultiplier)/maxbrow)/2
    if classifier > 0 and classifier > relaxcheek/maxcheek: #cheek percentage greater than brow
        classlabel.set("Positive")
        label.config(fg=color_blue)
        axes[1].axvline(x=classifier*maxcheek)
    elif classifier < 0 and classifier < -relaxbrow/maxbrow:
        classlabel.set("Negative")
        label.config(fg=color_red)
        axes[0].axvline(x=-classifier*maxbrow)
    else:
        classlabel.set("Neutral/Unknown")
        label.config(fg="black")
        if classifier < 0:
            axes[0].axvline(x=-classifier*maxbrow)
        else:
            axes[1].axvline(x=classifier*maxcheek)
    if recording:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        record.append([time, eyebrow,cheek,maxbrow,maxcheek,relaxbrow, relaxcheek, classlabel.get()])

#function that plots live data
def live_plotter(identifier='', pause_time=0.1):
    global pauseplay
    global maxcheek, maxbrow
    global browbuffer, cheekbuffer, HRbuffer
    if pauseplay:
        eyebrow, cheek, HRreading = read()
        #print(datetime.datetime.now())
        browbuffer.append(eyebrow)
        cheekbuffer.append(cheek)
        HRbuffer.append(HRreading)
        if len(browbuffer) == 1:
            axes[0].clear()
            axes[1].clear()
            if HRmode:
                HRmultiplier = HRreading/restHR
            else:
                HRmultiplier = 1
            if cheek*HRmultiplier > maxcheek:
                maxcheek = cheek*HRmultiplier
            if eyebrow*HRmultiplier > maxbrow:
                maxbrow = eyebrow*HRmultiplier
            axes[0].barh(0, eyebrow*HRmultiplier,  1,  align='center', color=color_red, zorder=10)
            axes[0].barh(0, eyebrow,  1,  align='center', color=color_blue, zorder=10)
            axes[1].barh(0, cheek*HRmultiplier,  1,  align='center', color=color_red, zorder=10)
            axes[1].barh(0, cheek, 1, align='center', color=color_blue, zorder=10)
            axissettings()
            classify(eyebrow,cheek,HRreading)
            browbuffer.clear() 
            cheekbuffer.clear()
            HRbuffer.clear()
        

#reset axis settings
def axissettings():
    axes[0].set_title(title0, fontsize=18, pad=15, color=color_red, **hfont)
    axes[1].set_title(title1, fontsize=18, pad=15, color=color_blue, **hfont)
    axes[1].set_xticks([0, round(maxcheek)])
    axes[1].set_xticklabels([0, round(maxcheek)])
    axes[0].set_xticks([0, round(maxbrow)])
    axes[0].set_xticklabels([0, round(maxbrow)])
    axes[0].invert_xaxis()
    axes[0].set(yticks=[-1, 0,1], yticklabels=['','',''])
    for label in (axes[0].get_xticklabels() + axes[0].get_yticklabels()):
        label.set(fontsize=13, color=font_color, **hfont)
    for label in (axes[1].get_xticklabels() + axes[1].get_yticklabels()):
        label.set(fontsize=13, color=font_color, **hfont)
    axes[0].axvline(x=relaxbrow, dashes = (4, 2), color = 'black')
    axes[1].axvline(x=relaxcheek, dashes = (4, 2), color = 'black')
        
HRmode = False
pauseplay = True

fEMG = serial.Serial(port='COM6', baudrate=9600, timeout=1)
heartrate = serial.Serial(port='COM5', baudrate=9600, timeout=0.1)
time.sleep(2)
print(heartrate.readline().decode())
data = fEMG.readline()

#customization settings
font_color = '#525252'
hfont = {'fontname':'Calibri'}
facecolor = '#eaeaf2'
color_red = '#fd625e'
color_blue = '#01b8aa'
title0 = 'Negative'
title1 = 'Positive'
LARGEFONT = ("Verdana", 35)
MEDFONT = ("Verdana", 20)

fig, axes = plt.subplots(figsize=(10,5), facecolor=facecolor, ncols=2, sharey=True)
fig.tight_layout()
plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.05, right=0.95)


emotrack = Tk()
canvas = FigureCanvasTkAgg(fig, emotrack)
canvas.get_tk_widget().grid(row = 2, column = 0, padx = 10, pady = 10)

classlabel = StringVar(value="Hello")
HRlabelvar = StringVar(value='HR Integration: OFF')
HRvar = StringVar(value='')
recordvar = StringVar(value = "Recording:OFF")

title = Label(emotrack, text="Emotion Sensor", font = LARGEFONT)
title.grid(row=0,column=0,padx=10,pady=10)
modelabel = Label(emotrack, textvariable = HRlabelvar, font = MEDFONT)
modelabel.grid(row=0,column=1,padx=10,pady=10)
label = Label(emotrack, bg='white', textvariable=classlabel, font = MEDFONT)
label.grid(row=1,column=0,padx=10,pady=10)
HRlabel = Label(emotrack, textvariable=HRvar, font = MEDFONT)
HRlabel.grid(row=1,column=1,padx=10,pady=10)
recordlabel = Label(emotrack, textvariable = recordvar, font = MEDFONT)
recordlabel.grid(row=2, column = 1, padx=10, pady=10)

button = Button(emotrack, text="Pause/Play", command = pause)
button.grid(row=3,column=0,padx=10,pady=10)
button = Button(emotrack, text = "Calibrate", command = calibrate)
button.grid(row=4,column=0,padx=10,pady=10)
button = Button(emotrack, text = "HR Mode", command = HRmodechange)
button.grid(row=5,column=0,padx=10,pady=10)
recordbutton = Button(emotrack, text = 'Start/Stop Recording', command = recordonoff)
recordbutton.grid(row=3, column = 1, padx = 10, pady=10)

ani = animation.FuncAnimation(fig,live_plotter, interval=250)
emotrack.mainloop()
fEMG.close()
heartrate.close()
# Importing Libraries
import serial
import matplotlib.pyplot as plt
import numpy as np

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
size = 10
x_vec = np.zeros(size)
y_vec = np.zeros(size)
line1 = []


def read():
    data = arduino.readline()
    if data:
        data_decoded = data.decode()
        num_list = data_decoded.strip().split()
        eyebrow = int(num_list[0])
        cheek = int(num_list[1])
    return eyebrow, cheek


# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')


def live_plotter(eyebrow, cheek, line1, identifier='', pause_time=0.1):
    if not line1:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(eyebrow, cheek, '-o', alpha=0.8)
        # update plot label/title
        plt.xlabel('Eyebrow')
        plt.ylabel('Cheek')
        plt.title('Title: {}'.format(identifier))
        plt.show()

    line1.set_xdata(eyebrow)
    line1.set_ydata(cheek)
    # adjust limits if new data goes beyond bounds
    if np.min(eyebrow) <= line1.axes.get_xlim()[0] or np.max(eyebrow) >= line1.axes.get_xlim()[1]:
        plt.xlim([np.min(eyebrow) - np.std(eyebrow), np.max(eyebrow) + np.std(eyebrow)])
    if np.min(cheek) <= line1.axes.get_ylim()[0] or np.max(cheek) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(cheek) - np.std(cheek), np.max(cheek) + np.std(cheek)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1


while True:
    eyebrow, cheek = read()
    line1 = live_plotter(x_vec, y_vec, line1)
    x_vec = np.append(x_vec[1:], eyebrow)
    y_vec = np.append(y_vec[1:], cheek)

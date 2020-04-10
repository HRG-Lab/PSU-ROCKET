#! /usr/bin/env python3
# I struggled getting this to run properly in a jupyter notebook, mostly due to the animations
# To run, you must ensure the correct serial device for the sensor in the line indicated below

import datetime as dt
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
from scipy.stats import norm

HISTORY_SIZE = 25
ser = serial.Serial('/dev/ttyACM0', 115200) # <--- Change this to correct port

readings = deque(maxlen=HISTORY_SIZE)
y_vals = deque(maxlen=HISTORY_SIZE)
x_vals = np.arange(400, 700, 1)

sd = 16.985
violet_pdf = lambda x: norm.pdf(x, 450, sd)
blue_pdf = lambda x: norm.pdf(x, 500, sd)
green_pdf = lambda x: norm.pdf(x, 550, sd)
yellow_pdf = lambda x: norm.pdf(x, 570, sd)
orange_pdf = lambda x: norm.pdf(x, 600, sd)
red_pdf = lambda x: norm.pdf(x, 650, sd)


def read_sensor(ser):
    data = ser.readline()
    if data == b'\r\n':
        data = ser.readline()
    data = data.split()
    if len(data) != 14:
        return None

    colors = {}
    colors['violet'] = int(data[3])
    colors['blue'] = int(data[5])
    colors['green'] = int(data[7])
    colors['yellow'] = int(data[9])
    colors['orange'] = int(data[11])
    colors['red'] = int(data[13])

    return colors


def gen_random_data():
    colors = {}
    colors['violet'] = np.random.uniform(low=0, high=1500)
    colors['blue'] = np.random.uniform(low=0, high=1500)
    colors['green'] = np.random.uniform(low=0, high=1500)
    colors['yellow'] = np.random.uniform(low=0, high=1500)
    colors['orange'] = np.random.uniform(low=0, high=1500)
    colors['red'] = np.random.uniform(low=0, high=1500)

    return colors


def gen_chart_data(reading):
    chart_data = [
        reading['violet'] * violet_pdf(x) + \
        reading['blue'] * blue_pdf(x) + \
        reading['green'] * green_pdf(x) + \
        reading['orange'] * orange_pdf(x) + \
        reading['red'] * red_pdf(x)
        for x in x_vals
    ]

    return chart_data


fig, ax = plt.subplots(1, 2)
plt.tight_layout()
ax[1].set_xlabel('Wavelength [nm]')
ax[1].set_ylabel('Time [+s]')

waterfall_size = 300
extent = [400, 700, 0, waterfall_size]
waterfall = np.zeros((waterfall_size, len(x_vals)))
im = plt.imshow(waterfall, interpolation='none', extent=extent)


def animate(i):
    global waterfall
    reading = read_sensor(ser)
    #reading = gen_random_data()
    if reading is not None:
        # Delete top row of data and append new data to bottom
        chart_data = gen_chart_data(reading)
        ax[0].cla()
        ax[0].plot(x_vals, chart_data)
        ax[0].set_xlabel('Wavelength [nm]')
        ax[0].set_ylabel('Relative magnitude')
        waterfall = np.delete(waterfall, 0, axis=0)
        waterfall = np.vstack((waterfall, np.array(chart_data)))

    im.set_array(waterfall)
    im.autoscale()
    return [im]
    # y_vals = [dt.datetime.now() + dt.timedelta(seconds=i) for i in range(len(readings))]


ani = FuncAnimation(fig, animate, interval=10)
plt.show()

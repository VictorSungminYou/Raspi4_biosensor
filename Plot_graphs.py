import tkinter
import matplotlib
from heartrate_monitor import HeartRateMonitor
import time
import argparse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import smbus

matplotlib.use('TkAgg')

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true", default=False,
                    help="print raw data instead of calculation result")
parser.add_argument("-t", "--time", type=int, default=30,
                    help="duration in seconds to read from sensor, default 30")
args = parser.parse_args()

# Define some constants from the datasheet
DEVICE     = 0x48 # Device address (A0-A2)
AIN0       = 0x40 # Address of AIN0
AIN1       = 0x41 # Address of AIN1
AIN2       = 0x42 # Address of AIN2
AIN3       = 0x43 # Address of AIN3

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def readADC(channel):
    bus.write_byte(DEVICE, channel) # write to device
    bus.read_byte(DEVICE) # read first byte (we discard this one)
    return bus.read_byte(DEVICE) # Read second byte and return it

# Set up the real-time plot
fig, ax = plt.subplots()
x_data, max_data = [], []
max_line, = ax.plot(x_data, max_data, label="BPM")

ain0_data, ain1_data, ain2_data, ain3_data = [], [], [], []
ain0_line, = ax.plot(x_data, ain0_data, label="AIN0")
ain1_line, = ax.plot(x_data, ain1_data, label="AIN1")
ain2_line, = ax.plot(x_data, ain2_data, label="AIN2")
ain3_line, = ax.plot(x_data, ain3_data, label="AIN3")

last_bpm = 0
last_time = 0

def update_plot(frame):
    x_data.append(last_time)
    max_data.append(last_bpm)

    # Read the four analog signals from the PCF8591 module
    ain0 = readADC(AIN0)
    ain1 = readADC(AIN1)
    ain2 = readADC(AIN2)
    ain3 = readADC(AIN3)

    # Plot the signals
    ain0_data.append(ain0)
    ain1_data.append(ain1)
    ain2_data.append(ain2)
    ain3_data.append(ain3)

    # Keep only the most recent 1,000 values
    if len(x_data) > 1000:
        x_data.pop(0)
        max_data.pop(0)
        ain0_data.pop(0)
        ain1_data.pop(0)
        ain2_data.pop(0)
        ain3_data.pop(0)

    max_line.set_xdata(x_data)
    max_line.set_ydata(max_data)
    ain0_line.set_xdata(x_data)
    ain0_line.set_ydata(ain0_data)
    ain1_line.set_xdata(x_data)
    ain1_line.set_ydata(ain1_data)
    ain2_line.set_xdata(x_data)
    ain2_line.set_ydata(ain2_data)
    ain3_line.set_xdata(x_data)
    ain3_line.set_ydata(ain3_data)

    ax.relim()
    ax.autoscale_view()

    ax.set_xticks([])
    ax.set_yticks([])

    ax.legend()
    return max_line, ain0_line, ain1_line, ain2_line, ain3_line,

def PPG_callback(bpm, spo2, time):
    global last_bpm, last_time
    last_bpm = bpm
    last_time = time

print('sensor starting...')
hrm = HeartRateMonitor(print_raw=args.raw, print_result=False, callback=PPG_callback)
hrm.start_sensor()

# Set up the animation
ani = FuncAnimation(fig, update_plot, blit=True, interval=10)

try:
    plt.show(block=True)
    time.sleep(args.time)
except KeyboardInterrupt:
    print('keyboard interrupt detected, exiting...')

hrm.stop_sensor()
print('sensor stoped!')

import time
import smbus
import matplotlib.pyplot as plt
import numpy as np

# Constants
DEVICE     = 0x48 # Device address (A0-A2)
ADC_CHNLS  = [0x40, 0x41, 0x42, 0x43] # ADC channels
N_SAMPLES  = 100

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

# Initialize plot
plt.ion() 
fig, ax = plt.subplots(4, 1, sharex=True)

# Initialize data arrays
data = np.zeros((4, N_SAMPLES))

def read_adc(channel):
    """Reads the ADC channel."""
    if channel in ADC_CHNLS:
        bus.write_byte(DEVICE, channel)
        bus.read_byte(DEVICE)  # dummy read to start conversion
        return bus.read_byte(DEVICE)
    else:
        raise ValueError('Invalid ADC channel.')

def main():
    try:
        while True:
            for i, channel in enumerate(ADC_CHNLS):
                value = read_adc(channel)
                print(f"Channel {channel - 0x40}: {value}")
                
                # Shift old data to the left
                data[i, :-1] = data[i, 1:]
                # Add new data to the right
                data[i, -1] = value
                
                # Update plot
                ax[i].clear()
                ax[i].plot(data[i])
                ax[i].set_title(f'Channel {channel - 0x40}')
            
            plt.pause(0.1)  # short pause for plots to update

    except KeyboardInterrupt:
        plt.close()

if __name__ == "__main__":
    main()

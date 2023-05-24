#!/usr/bin/env python3
import PCF8591 as ADC
import time


def setup():
    ADC.setup(0x48)

def loop():
	status = 1
	while True:
            print ('AIN0: %s AIN1: %s AIN2: %s AIN3: %s ' % (ADC.read(0), ADC.read(1), ADC.read(2), ADC.read(3)))
            time.sleep(0.2)

if __name__ == '__main__':
	try:
            setup()
            loop()
	except KeyboardInterrupt:
	    pass

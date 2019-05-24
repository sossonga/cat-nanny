#!/usr/bin/env python

"""Main script for the Cat Nanny project, to interface with the sensors"""

import RPi.GPIO as GPIO
import time

__author__ = "Sara Alsowaimel and Amanda Sossong"
__version__ = "1.0"
__date__ = "5/23/19"

def motionsensor():
    """The motionsensor function takes the input from the PIR sensor on pin 11 and
    prints to the console if motion is detected
    :return: nothing"""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.IN)

    while True:
        i = GPIO.input(11)
        if (i == 0):
            print("No intruders")
            time.sleep(0.2)
        elif (i == 1):
            print("Intruder alert!")
            time.sleep(0.2)


def main():
    """The main function calls on the sensors and inputs the data into a database
    :return: nothing"""
    motionsensor()


if __name__ == '__main__':
    main()



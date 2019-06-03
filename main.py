#!/usr/bin/env python

"""Main script for the Cat Nanny project, to interface with the sensors and servos"""

import serial
import RPi.GPIO as GPIO
import time
import sys

__author__ = "Sara Alsowaimel and Amanda Sossong"
__version__ = "1.0"
__date__ = "5/23/19"


def motionsensor():
    """The motionsensor function takes the input from the PIR sensor on pin 11 and
    prints to the console if motion is detected
    :return: nothing"""
    # clean up any GPIO settings before setting the motion sensor
    GPIO.cleanup()
    GPIO.setwarnings(False)

    # set mode to BOARD and GPIO pin 11 to input
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.IN)

    i = GPIO.input(11)
    # if sensor outputs 0, no motion detected
    if (i == 0):
        print("No one is here")
        time.sleep(0.2)
    # if sensor outputs 1, motion detected
    elif (i == 1):
        print("Cat is at the Cat Nanny!")
        time.sleep(0.2)


def tempreading():
    """The tempreading function takes the serial output from the Arduino and prints
    to the console every 1 second
    :return: nothing"""
    # read the serial port connection from the Arduino
    ser = serial.Serial('/dev/ttyACM0', 9600)
    print(ser.readline())


def servocontrol():
    """The servocontrol function defines the GPIO pins the two servos are connected to
    and controls their movements
    :return: nothing"""
    # define GPIO pins 20 and 21 for the food servo and play servo
    foodpin = 20
    playpin = 21
    # clean up any GPIO settings before setting the servos
    GPIO.cleanup()
    GPIO.setwarnings(False)
    # set mode to BCM and set pins 20 and 21 to output
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(foodpin, GPIO.OUT)
    GPIO.setup(playpin, GPIO.OUT)

    # set the PWM for food servo and play servo
    foodpwm = GPIO.PWM(foodpin, 50)
    playpwm = GPIO.PWM(playpin, 50)

    # initialize the servos
    foodpwm.start(2.5)
    playpwm.start(2.5)

    # run servos until a KeyboardInterrupt exception
    try:
        while True:
            foodpwm.ChangeDutyCycle(5)
            playpwm.ChangeDutyCycle(5)
            time.sleep(0.5)
    except KeyboardInterrupt:
        foodpwm.stop()
        playpwm.stop()


def consoleargs(arg):
    """The consoleargs function takes console input and compares it to a dictionary key. If the
    argument is valid, the corresponding function is run
    :return: none"""
    # define the arguments dictionary
    args = {
        "motionsensor": motionsensor,
        "tempreading": tempreading,
        "servocontrol": servocontrol,
        "exit": shutoff
    }
    # validate that the argument is valid and run the function
    func = args.get(arg, lambda: "Invalid command")
    print(func())


def shutoff():
    """The shutoff function cleans up the GPIO mode and setup and exits with code 0
    :return: none"""
    GPIO.cleanup()
    sys.exit()


def main():
    """The main function calls on the sensors and inputs the data into a database
    :return: nothing"""
    # take user input and print the output of the requested sensor
    while True:
        userinput = input("Enter the commands motionsensor, tempreading, or servocontrol\n")
        consoleargs(userinput)


if __name__ == '__main__':
    main()



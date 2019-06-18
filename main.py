#!/usr/bin/env python

"""Main script for the Cat Nanny project, to interface with the sensors and servos"""

import serial
import RPi.GPIO as GPIO
import time
import sys
import argparse

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
    tempread = open('tempread.txt', 'a+')
    for line in range(5):
        tempread.write(str(ser.readline()))
        tempread.write("\n")
    tempread.close()
    tempread = open('tempread.txt', 'r')
    #print(tempread.read())
    tempread.close()
    print(str(ser.readline()))
    ser.close()


def foodservo():
    """The foodservo function defines the GPIO pin the food servo is connected to
    and controls it's movement
    :return: nothing"""
    # define GPIO pin 20 for the food servo
    foodpin = 20
    # clean up any GPIO settings before setting the servo
    GPIO.cleanup()
    GPIO.setwarnings(False)
    # set mode to BCM and set pin 20 to output
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(foodpin, GPIO.OUT)

    # set the PWM for food servo
    foodpwm = GPIO.PWM(foodpin, 50)

    # initialize the servo
    foodpwm.start(2.5)

    # run servo until a KeyboardInterrupt exception
    try:
        while True:
            foodpwm.ChangeDutyCycle(15)
            time.sleep(5)
    except KeyboardInterrupt:
        foodpwm.stop()


def treatservo():
    """The treatservo function does the same as foodservo but in a different direction
    :return: nothing"""
    treatpin = 20
    GPIO.cleanup()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(treatpin, GPIO.OUT)

    treatpwm = GPIO.PWM(treatpin, 50)
    treatpwm.start(2.5)

    try:
        while True:
            treatpwm.ChangeDutyCycle(45)
            time.sleep(0.5)
    except KeyboardInterrupt:
        treatpwm.stop()


def playservo():
    """The playservo function defines the GPIO pin for the play toy servo 
    and controls it's movement
    :return: nothing"""
    # define GPIO pin 21 for the play servo
    playpin = 21
    # clean up any GPIO settings before setting the servo
    GPIO.cleanup()
    GPIO.setwarnings(False)
    # set mode to BCM and set pin 21 to output
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(playpin, GPIO.OUT)

    # set the PWM for the play servo
    playpwm = GPIO.PWM(playpin, 50)

    # initialize the servo
    playpwm.start(2.5)

    # run servo until a KeyboardInterrupt exception
    try:
        while True:
            playpwm.ChangeDutyCycle(5)
            time.sleep(0.5)
    except KeyboardInterrupt:
        playpwm.stop()
 

def consoleargs(arg):
    """The consoleargs function takes console input and compares it to a dictionary key. If the
    argument is valid, the corresponding function is run
    :return: none"""
    # define the arguments dictionary
    args = {
        "motion": motionsensor,
        "temp": tempreading,
        "feed": foodservo,
        "treat": treatservo,
        "play": playservo,
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


def _args():
    """The _args function uses the argparse library to parse the user's arguments
    :return: The command line arguments"""
    arg_parser = argparse.ArgumentParser(description='catnanny lets the owner feed, treat, play with, and check on their cat')
    arg_parser.add_argument('action',
                            choices=['feed', 'treat', 'play'],
                            default='feed',
                            help='Action you want Cat Nanny to do')
    return arg_parser.parse_args()


def main():
    """The main function calls on the sensors and inputs the data into a database
    :return: nothing"""
    # take the command line argument and call the requested function
    args = _args()
    consoleargs(args.action)


if __name__ == '__main__':
    main()



#!/usr/bin/env python

"""Main script for the Cat Nanny project, to interface with the sensors and servos"""

import serial
import RPi.GPIO as GPIO
import time
import sys
import sqlite3
from datetime import datetime

__author__ = "Sara Alsowaimel and Amanda Sossong"
__version__ = "1.0"
__date__ = "5/23/19"


def _set_gpio():
    """The _set_gpio method sets the mode to BCM and disables warnings for the GPIO pins
    :return: nothing"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    return


def _clean_gpio():
    """The _clean_gpio method cleans up the GPIO settings
    :return: nothing"""
    GPIO.cleanup()
    return


def motionsensor():
    """The motionsensor function takes the input from the PIR sensor on pin 11 and
    prints to the console if motion is detected
    :return: nothing"""
    # do not show warnings
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

    _clean_gpio()
    return i


def tempreading():
    """The tempreading function takes the serial output from the Arduino and prints
    to the console every 1 second
    :return: nothing"""
    # read the serial port connection from the Arduino
    ser = serial.Serial('/dev/ttyACM0', 9600)

    reading = ser.readline().decode('utf-8')
    print(reading)

    ser.close()
    return reading


def servo(type):
    """The servo function defines the GPIO pin the food servo is connected to
    and controls it's movement
    :return: nothing"""
    # connect to DB and insert into sensor_data when the food button is clicked
    conn = sqlite3.connect("cat-nanny.db")
    c = conn.cursor()
    current_timestamp = datetime.now().isoformat()
    c.execute("""INSERT INTO sensor_data VALUES (?, ?, ?)""", (current_timestamp, type, 1))
    conn.commit()
    conn.close()

    # define GPIO pin 12 for the play servo
    if type == 'play':
        pin = 12
    # define pin 13 for food/treats
    else:
        pin = 13

    _set_gpio()
    GPIO.setup(pin, GPIO.OUT)

    # set the PWM for servo and initialize
    pwm = GPIO.PWM(pin, 50)
    pwm.start(2.5)

    try:
        # run servo
        if type == 'feed':
            pwm.ChangeDutyCycle(15)

        elif type == 'treat':
            pwm.ChangeDutyCycle(10)

        elif type == 'play':
            for i in range(20):
                pwm.ChangeDutyCycle(7.5)
                time.sleep(1)
                pwm.ChangeDutyCycle(2.5)
                time.sleep(1)
                pwm.ChangeDutyCycle(12.5)
                time.sleep(1)
        else:
            raise Exception

    except KeyboardInterrupt:
        _clean_gpio()
        sys.exit()

    except:
        _clean_gpio()
        print("An error has occurred")
        sys.exit()

    finally:
        time.sleep(5)
        pwm.stop()

    _clean_gpio()

    return


def query(sensor):
    """The query function queries the DB for the value of a sensor from the sensor_data table
    :return: The result of the query"""
    conn = sqlite3.connect("cat-nanny.db")
    c = conn.cursor()
    c.execute("""SELECT reading_value FROM sensor_data WHERE sensor = ? ORDER BY timestamp DESC LIMIT 1""", (sensor,))
    result = c.fetchone()
    conn.close()

    return result[0].strip()


def stat_query(sensor):
    """The stat_query function queries the DB for the count of a sensor's value equaling 1
    :return: The result of the query"""
    conn = sqlite3.connect("cat-nanny.db")
    c = conn.cursor()
    c.execute("""SELECT COUNT(*) FROM sensor_data WHERE sensor = ? AND reading_value = 1""", (sensor,))
    result = c.fetchone()
    conn.close()

    return result


def login(email, password):
    """The login function takes the email and password input from the app and checks if the
    credentials are in the DB
    :return: The result of the query"""
    conn = sqlite3.connect("cat-nanny.db")
    c = conn.cursor()
    c.execute("""SELECT COUNT(*) FROM user WHERE email = ? AND password = ?""", (email, password,))
    result = c.fetchone()
    conn.close()

    return result


def signup(email, password):
    """The signup function takes the email and password input from the signup page of the app
    and inserts the values into the DB
    :return: nothing"""
    conn = sqlite3.connect("cat-nanny.db")
    c = conn.cursor()
    c.execute("""INSERT INTO user VALUES (?, ?)""", (email, password))
    conn.commit()
    conn.close()

    return


def main():
    """The main function does nothing, all calls are made from the flask server, flasktest.py
    :return: nothing"""


if __name__ == '__main__':
    main()



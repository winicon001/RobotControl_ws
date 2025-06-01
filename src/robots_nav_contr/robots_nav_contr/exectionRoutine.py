#!/usr/bin/env python3
# File name   : redEye_MainRoutine.py
# Description : Main Robot Routine
# Product     : redEye  
# E-mail      : winicon@live.com
# Author      : Semiu ADEBAYO
# Date        : 2025/04/26
# credit      : Copyright (c) 2025 Semiu ADEBAYO
# Description : 
                # This script is used to read data from an Arduino and ESP32, process the data, and log it.
#               # It uses the rclpy library for ROS2 communication and pyodbc for database connection.
#               # The script includes error handling and logging to provide information about the connection status, data processing, and any errors that occur.This routine is to create overall logic for the robot's operation.
                # It subscribes to the topic /redEye_Arduino_data to read Arduino sensors Data
                # It also collates the sensors data  from arduino on topi redEye_Arduino_data
                # and sensor data from ESP32 on serial port, put them in structured arrays and assignemnt that 
                # can be used for commands, interlocks and control conditions

import RPi.GPIO as GPIO
import time
import rclpy
from rclpy.node import Node
import rclpy.logging
from std_msgs.msg import String
# from robots_nav_contr import esp32_serialData
from robots_nav_contr import Datalog

from robots_nav_contr import encoders
from robots_nav_contr import move

from robots_nav_contr import arduinosensorsdata
from robots_nav_contr import MainRoutine

import rclpy.logging

################################################################

import serial
import time
global esp_data



################################################
############## Robot Parameters ################

speed = 50  # Robot Speed
#################################################
# MPU6050 Data YPR
#################################################

robot = MainRoutine.DataSubscriber()
# rclpy.init()
def robotmainroutine():
    init_yaw = 0

    # Encoders Readings
    arduino_read_values = arduinosensorsdata.reading.checkdata()

    # Change obstacle distance based on environmental features
    if robot.ULTRASENSOR_DIST <= 25.0:
        move.move(speed, direction="backward", turn="left")

        return

    else:
        move.move(speed, direction = "forward", turn = "")
        time.sleep(2)
        # move.move(speed, direction = "forward", turn = "right")

    robotmainroutine()
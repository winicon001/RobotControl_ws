# File name   : encoders.py
# Description : Python Wheel Encoder code for LM393 H2010
# Product     : smilebot  
# E-mail      : winicon@live.com
# Author      : Semiu ADEBAYO
# Date        : 2024/08/15
# credit      : SciJoy @ https://www.youtube.com/watch?v=cLtMcqRetO0&t=101s

import RPi.GPIO as GPIO
import time
#from adafruit_Motorkit import Motorkit

# Encoders Pins Declaration
leftencoder = 15
rightencoder = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(leftencoder, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(rightencoder, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


Encoder1StateLast = GPIO.input(leftencoder)
enc1_revCount = 0

enc1count = 0           # Left wheel Total Revolution
enc1countTotal = 0      # Left wheel Total Encoder Ticks count

Encoder2StateLast = GPIO.input(rightencoder)
enc2_revCount = 0
enc2count = 0           # Right wheel Total Revolution
enc2countTotal = 0      # Right wheel Total Encoder Ticks count

    
def enc():

    global wheelCircumference

    global Encoder1StateLast
    global enc1count        # Left wheel Total Revolution
    global enc1countTotal   # Left wheel Total Encoder Ticks count
    global enc1_revCount

    global Encoder2StateLast
    global enc2count        # Right wheel Total Revolution
    global enc2countTotal   # Right wheel Total Encoder Ticks count
    global enc2_revCount
    global enc_data


    wheelCircumference = 215                # Wheel Circumference in mm (changed from 204 to 215)
    EncodercountPerRev = 40                 # Encoder Count Per Wheel Encoder1rotation
    dist_per_tic = wheelCircumference/EncodercountPerRev # Calculating the Encoder1distan

    Encoder1StateCurrent = GPIO.input(leftencoder)
    if Encoder1StateCurrent != Encoder1StateLast: # If the read value is different from the previous
        Encoder1StateLast = Encoder1StateCurrent # Increment the count
        enc1count +=1
        enc1countTotal +=1
    
    if enc1count == EncodercountPerRev:
        enc1_revCount +=1
        enc1count = 0
    
    Encoder1distance = dist_per_tic * enc1countTotal

    Encoder2StateCurrent = GPIO.input(rightencoder)
    if Encoder2StateCurrent != Encoder2StateLast: # If the read value is different from the previous
        Encoder2StateLast = Encoder2StateCurrent # Increment the count
        enc2count +=1
        enc2countTotal +=1
        
    if enc2count == EncodercountPerRev:
        enc2_revCount +=1
        enc2count = 0
    
    Encoder2distance = dist_per_tic * enc2countTotal
    enc_data = [enc1count, enc1countTotal, enc1_revCount, round(Encoder1distance, 2), enc2count, enc2countTotal, enc2_revCount, round(Encoder2distance, 2)]

    

    # print('enc1count= ', enc1count  , end=' ')
    # print('enc1countTotal= ', enc1countTotal, end=' ')
    # print('RevCount_L= ', enc1_revCount , end= ' ')
    # print('Encoder1distance= ', round(Encoder1distance, 2) , 'mm', end= '')
    # print('enc2count= ', enc2count  , end=' ')
    # print('enc2countTotal= ', enc2countTotal, end=' ')
    # print('RevCount_R= ', enc2_revCount , end= ' ')
    # print('Encoder2distance= ', round(Encoder2distance, 2), 'mm')

    return enc_data

    #except KeyboardInterrupt: # If CTRL+C is pressed
       # kit.motor1.throttle = 0
        #GPIO.cleanup() # End the Process

if __name__ == "__main__":
    # init()
    while True:
        # enc()
        print(enc(), enc()[0])
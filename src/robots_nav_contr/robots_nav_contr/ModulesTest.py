import encoders
import move
import time
import RPi.GPIO as GPIO
import ultra

while True:
    move.setup()
    move.move(100, 'forward', 'no', 1)
    #encoders.wheelEncodersReading()
    ultra.checkdist()


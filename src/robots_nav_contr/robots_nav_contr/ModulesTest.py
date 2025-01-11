import encoders
import move
import time
import RPi.GPIO as GPIO
import ultra_2

speed = 100

move.setup()

while True:

    arduino_read_value = ultra_2.reading.checkdist()

    # Remove String character from Sensor readings from ESP32
    numeric_part = ''.join(char for char in arduino_read_value if char.isdigit() or char == '.')

    # Remove white space from Sensor readings from ESP32
    clean_part = numeric_part.strip().replace(' ', '')

    # Convert Sensor readings from ESP32 to float data type
    obstacle_dist = float(clean_part)

    # print("Message is :  ", arduino_read_value)
    # print("Message is :  ", obstacle_dist, end = " ")
    
    
    if (obstacle_dist <= 10.0):
        move.move(speed, direction = "backward", turn = "left")
        print('obstacle at: ', obstacle_dist, '|', end = ' ')
        encoders.enc()
        

    
    else:
        move.move(speed, direction = "forward", turn = "")
        print('obstacle at: ', obstacle_dist, '|', end = ' ')
        encoders.enc()

    

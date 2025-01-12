#!/usr/bin/env python3
import serial

class reading:
    def checkdist():
        arduino_port = '/dev/ttyUSB0'  # Adjust this based on your actual port
        baud_rate = '115200'
        with serial.Serial(arduino_port, baud_rate) as ser:
            user_input = "1" # Start Data Reading from MPU6050
            ser.write(user_input.encode())
            data = ser.readline().decode().strip()
            print("Distance =  ", data)
            return data

    def checkdata():
        arduino_port = '/dev/ttyUSB0'  # Adjust this based on your actual port
        baud_rate = '115200'
        with serial.Serial(arduino_port, baud_rate) as ser:
            user_input = "1" # Start Data Reading from MPU6050
            ser.write(user_input.encode())
            data = ser.readline().decode().strip()
            measuredValues = data.split(",")
            # print(f"Received sensor values: {measuredValues}")
            #print("distance: ", measuredValues[0],"Yaw: ", measuredValues[1])
            return measuredValues

    def checkdata2():
        arduino_port = '/dev/ttyUSB0'  # Adjust this based on your actual port
        baud_rate = '115200'
        with serial.Serial(arduino_port, baud_rate) as ser:
            user_input = "1" # Start Data Reading from MPU6050
            ser.write(user_input.encode())
            data = ser.readline().decode().strip()
            measuredValues = data.split(",")
            # print(f"Received sensor values: {measuredValues}")
            print("distance: ", measuredValues[0],"Yaw: ", measuredValues[1])
            return measuredValues
            
    
    
    def receivedata():
        ser = serial.Serial('/dev/ttyUSB0', 115200)  # Adjust port name as needed
        user_input = "1" # Start Data Reading from MPU6050
        ser.write(user_input.encode())
        while True:
            data = ser.readline().decode().strip()
            measuredValues = data.split(",")
            print(f"Received sensor values: {measuredValues}")
            print("Yaw: ", measuredValues[0])    



if __name__ == '__main__':
    while True:
        # reading.receivedata()
        # reading.checkdist()
        reading.checkdata2()






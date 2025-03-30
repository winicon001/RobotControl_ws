import serial

class reading:
    def checkdist():
        arduino_port = '/dev/ttyUSB0'  # Adjust this based on your actual port
        baud_rate = '115200'
        with serial.Serial(arduino_port, baud_rate) as ser:
            data = ser.readline().decode().strip()
            # print("Distance =  ", data)
            return data

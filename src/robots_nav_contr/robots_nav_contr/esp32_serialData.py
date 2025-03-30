import serial

#################################################
# MPU6050 Data YPR
#################################################

error_flag = False  # Error detection flag for transfered data

startup_command = "go"
ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0', 9600, timeout=5) #  Corresponding to /ttyUSB1

ser.write(bytes(startup_command.encode("utf-8")))  # Send data to ESP32 to start pulling gyroscope data. This is introduced due to the
                                                   # default MPU6050 sketch which look for a starting command of any character over the serial line.

# Read Data from ESP32
def read_data():
    values = ser.readline()
    if isinstance(values, bytes):
        try:
            decoded_value = values.decode('utf-8', errors='ignore')  # Ignore errors and noice in sensor data
        except UnicodeDecodeError:
            print("Invalid data detected.")
            error_flag = True
        else:
            error_flag = False
            print("Not a byte object.")

    print(values)
    print ("Read Gyro data: " + decoded_value + " from ESP32", end='\n')
    return decoded_value

# Write Data to ESP32
def write_data():
    ser.write(".")  # Send data to Arduino

# while 1:
#     read_data()

if __name__== '__main__':
    read_data()
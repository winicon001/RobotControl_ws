#!/usr/bin/env python3

import time
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from robots_nav_contr import esp32_serialData

################################################################

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

    print(decoded_value)
    # print ("Read Gyro data: " + decoded_value + " from ESP32", end='\n')
    return decoded_value

# Write Data to ESP32
def write_data():
    ser.write(bytes(startup_command.encode("utf-8")))  # Send data to Arduino



###################################################################################



class DataSubscriber(Node):
    def __init__(self):
        super().__init__('Arduino_DataReadout')

        # Subscribe to the output topic
        self.subscription = self.create_subscription(
            String,
            '/arduino_data',
            self.callback,
            10
        )

    def callback(self, msg):
        esp_data = read_data()

        # Split Arduino the data into component parts
        esp_values = esp_data.split(",")

        # Process the data received
        self.get_logger().info(f'Received final data: {msg.data}')
        data_ = msg.data

    
        # Split Arduino the data into component parts
        measuredValues = data_.split(",")
        ENC_TOTAL_COUNT_L = measuredValues[0]
        ENC_TOTAL_COUNT_R = measuredValues[1]
        COUNTER_L = measuredValues[2]
        COUNTER_R = measuredValues[3]
        rotation1 = measuredValues[4]
        rotation2 = measuredValues[5]



        print("enc_L : ", ENC_TOTAL_COUNT_L, '|', end = ' ')
        print("enc_R : ", ENC_TOTAL_COUNT_R, '|', end = ' ')
        print("count_L : ", COUNTER_L, '|', end = ' ')
        print("count_R : ", COUNTER_R, '|', end = ' ')
        print("rotation1 : ", rotation1, '|', end = ' ')
        print("rotation2 : ", rotation2)
        print(esp_values)
        return data_


    
    



def main(args=None):
    print('.... Initialising ROS2 Node. Please Wait')
    time.sleep(2)
    print('.... Starting Serial Comms to ESP32 Node. Initialisation in Progress')
    write_data()
    time.sleep(10)
    print('.... Starting ROS2 Node ........')

    rclpy.init(args=args)
    time.sleep(10)
    print('....Emptying Wrong Buffer Data from ESP32 ........ Please wait While ROS Node starts')

    node = DataSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

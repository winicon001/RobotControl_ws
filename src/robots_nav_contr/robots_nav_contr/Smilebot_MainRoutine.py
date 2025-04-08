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
    # Declaration of Local Variables

    ULTRASENSOR_DIST = 0.0
    YAW = 0.0
    PITCH = 0.0
    ROLL = 0.0
    
    ENC_TOTAL_COUNT_L = 0.0
    ENC_TOTAL_COUNT_R = 0.0
    COUNTER_L = 0.0
    COUNTER_R = 0.0
    rotation1 = 0.0
    rotation2 = 0.0



    def __init__(self):
        super().__init__('Arduino_DataReadout')

        # Subscribe to the output topic
        self.subscription = self.create_subscription(
            String,
            '/SmileBot_Arduino_data',
            self.callback,
            10
        )

    def callback(self, msg):

        ##############################################
        ########## Sensors Data ######################
        esp_data = read_data()
        esp_data = esp_data if esp_data else [] # Use empty array If data is not available 

        # Split Arduino the data into component parts
        esp_values = esp_data.split(",")
        data_bundle = len(esp_values) # Length of data from Arduino

        # Check that data from ESP32 exists and not empty
        if esp_data:
            try:
                if len(esp_values) > 3:
                    self.get_logger().info(f'Received complete MPU6050 data from esp32. Items in the List Received : {data_bundle}')
                    ULTRASENSOR_DIST = esp_values[0]
                    YAW              = esp_values[1]
                    PITCH            = esp_values[2]
                    ROLL             = esp_values[3]

                # Data Error Correction
                else:
                    if len(esp_values) == 3:
                        self.get_logger().warning(f'Warning!. Incomplete MPU6050 data from esp32. Items in the List Received : {data_bundle}')
                        ULTRASENSOR_DIST = esp_values[0]
                        YAW              = esp_values[1]
                        PITCH            = esp_values[2]
                        ROLL             = 0.0
                    if len(esp_values) == 2:
                        ULTRASENSOR_DIST = esp_values[0]
                        YAW              = esp_values[1]
                        PITCH            = 0.0
                        ROLL             = 0.0
                    if len(esp_values) == 1:
                        ULTRASENSOR_DIST = esp_values[0]
                        YAW              = 0.0
                        PITCH            = 0.0
                        ROLL             = 0.0
                    if len(esp_values) == 0:
                        ULTRASENSOR_DIST = 0.0
                        YAW              = 0.0
                        PITCH            = 0.0
                        ROLL             = 0.0

            except IndexError:
                self.get_logger().error('Error: IndexError occurred while accessing MPU6050 data.')

        else:
            self.get_logger().warning('Warning: Data bundle from MPU6050 is empty or missing items.')


        # Process the data received
        self.get_logger().info(f'Received final data: {msg.data}')

        # Split Arduino the data into component parts        
        data_ = msg.data
        data_ = data_ if data_ else [] # Use empty array If data is not available 

        measuredValues = data_.split(",")
        data_bundle2 = len(measuredValues) # Length of data from Arduino

         # Check that data from Arduino exists and not empty
        if data_:
            try:
                if data_bundle2 > 5:
                    self.get_logger().info(f'Received complete Arduino data. Items in the List Received : {data_bundle2}')
                    ENC_TOTAL_COUNT_L = measuredValues[0]
                    ENC_TOTAL_COUNT_R = measuredValues[1]
                    COUNTER_L = measuredValues[2]
                    COUNTER_R = measuredValues[3]
                    rotation1 = measuredValues[4]
                    rotation2 = measuredValues[5]

                # Data Error Correction
                else:
                    if data_bundle2 == 5:
                        self.get_logger().warning(f'Warning!. Incomplete Arduino Data. Items in the List Received : {data_bundle2}')
                        ENC_TOTAL_COUNT_L = measuredValues[0]
                        ENC_TOTAL_COUNT_R = measuredValues[1]
                        COUNTER_L = measuredValues[2]
                        COUNTER_R = measuredValues[3]
                        rotation1 = measuredValues[4]
                        rotation2 = 0.0
                    if data_bundle2 == 4:
                        self.get_logger().warning(f'Warning!. Incomplete Arduino data. Items in the List Received : {data_bundle2}')
                        ENC_TOTAL_COUNT_L = measuredValues[0]
                        ENC_TOTAL_COUNT_R = measuredValues[1]
                        COUNTER_L = measuredValues[2]
                        COUNTER_R = measuredValues[3]
                        rotation1 = 0.0
                        rotation2 = 0.0
                    if data_bundle2 == 3:
                        self.get_logger().warning(f'Warning!. Incomplete Arduino data. Items in the List Received : {data_bundle2}')
                        ENC_TOTAL_COUNT_L = measuredValues[0]
                        ENC_TOTAL_COUNT_R = measuredValues[1]
                        COUNTER_L = measuredValues[2]
                        COUNTER_R = 0.0
                        rotation1 = 0.0
                        rotation2 = 0.0
                    if data_bundle2 == 2:
                        self.get_logger().warning(f'Warning!. Incomplete Arduino data. Items in the List Received : {data_bundle2}')
                        ENC_TOTAL_COUNT_L = measuredValues[0]
                        ENC_TOTAL_COUNT_R = measuredValues[1]
                        COUNTER_L = 0.0
                        COUNTER_R = 0.0
                        rotation1 = 0.0
                        rotation2 = 0.0

                    if data_bundle2 == 1:
                        self.get_logger().warning(f'Warning!. Incomplete Arduino data. Items in the List Received : {data_bundle2}')
                        ENC_TOTAL_COUNT_L = measuredValues[0]
                        ENC_TOTAL_COUNT_R = 0.0
                        COUNTER_L = 0.0
                        COUNTER_R = 0.0
                        rotation1 = 0.0
                        rotation2 = 0.0
            except IndexError:
                self.get_logger().error('Error: IndexError occurred while accessing Arduino data.')
        else:
            self.get_logger().warning('Warning: Data bundle from Arduino is empty or missing items.')


        ##############################################


        print("enc_L : ", ENC_TOTAL_COUNT_L, '|', end = ' ')
        print("enc_R : ", ENC_TOTAL_COUNT_R, '|', end = ' ')
        print("count_L : ", COUNTER_L, '|', end = ' ')
        print("count_R : ", COUNTER_R, '|', end = ' ')
        print("rotation1 : ", rotation1, '|', end = ' ')
        print("rotation2 : ", rotation2)

        print("UltraSensor Distance : ", esp_values[0], '|', end = ' ')
        print("Yaw : ", esp_values[1], '|', end = ' ')
        print("Pitch : ", esp_values[2], '|', end = ' ')
        print("Roll : ", esp_values[3])

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

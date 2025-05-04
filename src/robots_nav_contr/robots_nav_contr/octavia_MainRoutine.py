#!/usr/bin/env python3
# File name   : octavia_MainRoutine.py
# Description : Main Robot Routine
# Product     : octavia  
# E-mail      : winicon@live.com
# Author      : Semiu ADEBAYO
# Date        : 2025/04/04
# credit      : Copyright (c) 2024 Semiu ADEBAYO
# Description : 
                # This script is used to read data from an Arduino and ESP32, process the data, and log it.
#               # It uses the rclpy library for ROS2 communication and pyodbc for database connection.
#               # The script includes error handling and logging to provide information about the connection status, data processing, and any errors that occur.This routine is to create overall logic for the robot's operation.
                # It subscribes to the topic /octavia_Arduino_data to read Arduino sensors Data
                # It also collates the sensors data  from arduino on topi octavia_Arduino_data
                # and sensor data from ESP32 on serial port, put them in structured arrays and assignemnt that 
                # can be used for commands, interlocks and control conditions

import time
import time
import rclpy
from rclpy.node import Node
import rclpy.logging
from std_msgs.msg import String
from robots_nav_contr import esp32_serialData
from robots_nav_contr import Datalog
from robots_nav_contr import odometry

################################################################

import serial
global esp_data

robotName = "octavia"  # Robot Name
robotID = "001"  # Robot ID
robotType = "octavia"  # Robot Type
robotVersion = "v1.0"  # Robot Version
robotSerial = "PRX3OQTSEM"  # Robot Serial Number
robotManufacturer = "WiniCon"  # Robot Manufacturer

#################################################
# MPU6050 Data YPR
#################################################
baud = 115200

robot_data = {}

error_flag = False  # Error detection flag for transfered data

startup_command = "go"
ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0', baud, timeout=5) #  Corresponding to /ttyUSB1

ser.write(bytes(startup_command.encode("utf-8")))  # Send data to ESP32 to start pulling gyroscope data. This is introduced due to the
                                                   # default MPU6050 sketch which look for a starting command of any character over the serial line.

# Read Data from ESP32
def read_data():
    values = ser.readline()


    if isinstance(values, bytes):
        try:
            # Decode the byte object to a string
            decoded_value = values.decode('utf-8', errors='ignore')  # Ignore errors and noice in sensor data

            # Clean the decoded string           
            cleaned_value = decoded_value.strip()  # Remove leading and trailing whitespace
            cleaned_value = cleaned_value.replace('\r', '')  # Remove carriage return characters
            cleaned_value = cleaned_value.replace('\n', '')  # Remove newline characters
            ESP32_Logs.info('Valid and printable Data received.')
            ESP32_Logs.info('Decoded data packet from ESP32 successfully')
            
        except AttributeError:
            ESP32_Logs.warning('Attribute Error: Failed to decode the byte object.')
            # decoded_value = None
            
            error_flag = True
        except TypeError:
            ESP32_Logs.warning('Type Error: Failed to decode the byte object.')
            # decoded_value = None
            error_flag = True
        except ValueError:
            ESP32_Logs.warning('Value Error: Failed to decode the byte object.')
            # decoded_value = None
            error_flag = True
        except OverflowError:
            ESP32_Logs.warning('Overflow Error: Failed to decode the byte object.')
            # decoded_value = None            
            error_flag = True
        except IndexError:
            ESP32_Logs.warning('Index Error: Failed to decode the byte object.')
            # decoded_value = None            
            error_flag = True
        except UnicodeDecodeError:
            ESP32_Logs.warning('Uninicode Error: Failed to decode the byte object.')
            # decoded_value = None            
            error_flag = True
    else:
        error_flag = False
        # decoded_value = None
        ESP32_Logs.error('Error: Received data is not a byte object.')

    return cleaned_value


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

    speed_L = 0
    speed_R = 0
    totalDist_L = 0
    totalDist_R = 0

    def __init__(self):
        super().__init__('Octavia_Arduino_DataReadout')

        # Subscribe to the output topic
        self.subscription = self.create_subscription(
            String,
            '/octavia_Arduino_data',
            self.callback,
            10
        )

    def callback(self, msg):

        # Read Unltrasonic Sensor Distance Data from Arduino
        # The Data is sent from Arduino to ROS2 via the topic /octavia_Arduino_data
        # and subscribed to by this node - Octavia_Arduino_DataReadout

        dist_ = self.subscription
        dist_ = msg.data
        self.get_logger().info(f"Ultrasonic Distance from Arduino: {dist_}")

        ##############################################
        ########## Sensors Data ######################
        esp_data = read_data()
        esp_data = esp_data if esp_data else [] # Use empty array If data is not available 

        # Split Arduino the data into component parts
        esp_values = esp_data.split(",")
        data_bundle = len(esp_values) # Length of data from Arduino

        # Sample sensor data
        sample_data =  [151, 154, 454, 57963, 25, 455, 50.92, 13.0, 12455.8, 8320, 3295, 2312, 234, 2.0, 25676.8, 27]

        # Check that data from ESP32 exists and not empty
        if len(esp_values) > 1:
            try:
                if len(esp_values) > 15:
                    self.get_logger().info(f'Received complete data from esp32. Items in the List Received : {data_bundle}')
                    self.get_logger().info(f'Received complete data from esp32 : {esp_values}')
                    ULTRASENSOR_DIST = dist_
                    YAW              = esp_values[1]
                    PITCH            = esp_values[2]
                    ROLL             = esp_values[3]
                    ENC_TOTAL_COUNT_L = esp_values[4]
                    ENC_TOTAL_COUNT_R = esp_values[5]
                    COUNTER_L         = esp_values[6]
                    COUNTER_R         = esp_values[7]
                    rotation1         = esp_values[8]
                    rotation2         = esp_values[9]
                    speed_L           = esp_values[10]
                    speed_R           = esp_values[11]
                    dist_L            = esp_values[12]
                    dist_R            = esp_values[13]
                    totalDist_L       = esp_values[14]
                    totalDist_R       = esp_values[15]

                # Data Error Correction
                else:
                    if len(esp_values) < 16:
                        self.get_logger().warning(f'Warning!. Incomplete MPU6050 data from esp32. Items in the List Received : {data_bundle}')
                        self.get_logger().warning(f'Warning!. Data from esp32 : {esp_values}')
                        ULTRASENSOR_DIST = dist_  
                        YAW              = 0.0
                        PITCH            = 0.0
                        ROLL             = 0.0
                        ENC_TOTAL_COUNT_L = 0.0
                        ENC_TOTAL_COUNT_R = 0.0
                        COUNTER_L         = 0.0
                        COUNTER_R         = 0.0
                        rotation1         = 0.0
                        rotation2         = 0.0         
                        speed_L           = 0.0
                        speed_R           = 0.0
                        dist_L            = 0.0
                        dist_R            = 0.0
                        totalDist_L       = 0.0
                        totalDist_R       = 0.0

                
                # Assign the values to the class variables
                self.ULTRASENSOR_DIST = dist_
                self.YAW = YAW
                self.PITCH = PITCH
                self.ROLL = ROLL
                self.ENC_TOTAL_COUNT_L = ENC_TOTAL_COUNT_L
                self.ENC_TOTAL_COUNT_R = ENC_TOTAL_COUNT_R
                self.COUNTER_L = COUNTER_L
                self.COUNTER_R = COUNTER_R
                self.rotation1 = rotation1
                self.rotation2 = rotation2
                self.speed_L = speed_L
                self.speed_R = speed_R
                self.dist_L = dist_L
                self.dist_R = dist_R
                self.totalDist_L = totalDist_L
                self.totalDist_R = totalDist_R  

                # Create a data bundle
                # ESP32 data
                self.esp_data = [ULTRASENSOR_DIST, 
                                 YAW, PITCH, ROLL,
                                ENC_TOTAL_COUNT_L,
                                ENC_TOTAL_COUNT_R,
                                COUNTER_L,
                                COUNTER_R,
                                rotation1,
                                rotation2,  
                                speed_L,
                                speed_R,
                                dist_L,
                                dist_R,
                                totalDist_L,
                                totalDist_R
                                ][:16]  # Limit to 16 items to avoid overflow
  

            except IndexError:
                self.get_logger().error('Error: IndexError occurred while accessing MPU6050 data.')

        else:
            if not esp_data or len(esp_data) < 4:
                self.get_logger().warning('Warning: Data bundle from MPU6050 is empty or missing items.')


        # Generate Robot Details
        robot_details = [robotName,
                         robotID,
                         robotType,
                         robotVersion,
                         robotSerial,
                         robotManufacturer]

        ##############################################
        # self.get_logger().info(f'Data from Arduino {self.arduino_data}')
        self.get_logger().info(f'Data from ESP32 {self.esp_data}')

        # Data to Log   
        log_Data = [*robot_details,
                    *self.esp_data,
                    ]
        
        # ##########################################
        # Robot Data. This is the data that will be sent to the database
        # and used for commands, interlocks and control conditions
        # Also to identify the robot and its type
        # ###########################################
        robot_data['robotName'] = robotName
        robot_data['robotID'] = robotID
        robot_data['robotType'] = robotType
        robot_data['robotVersion'] = robotVersion
        robot_data['robotSerial'] = robotSerial
        robot_data['robotManufacturer'] = robotManufacturer
        robot_data['robotData'] = [
            'ULTRASENSOR_DIST',
            'YAW',
            'PITCH',
            'ROLL',
            'ENC_TOTAL_COUNT_L',
            'ENC_TOTAL_COUNT_R',
            'COUNTER_L',
            'COUNTER_R',
            'rotation1',
            'rotation2',
            'speed_L',
            'speed_R',
            'dist_L',
            'dist_R',
            'totalDist_L',
            'totalDist_R'
        ]
        # ##########################################


        # ##########################################
        # Odometry Calculation
        Odometry_logs.info('Starting Odometry Calculation')
        # Initialize the odometry with wheel radius and wheel base
        Routine_Message.info(' Odometry and Sensor Data Collection Node is Starting')
        odometry.MainRoutine(wheel_base=0.5, wheel_radius=0.1, left_wheel_speed=speed_L, right_wheel_speed=speed_R, dt=0.1)

        # ##########################################
        # ##########################################
        # Log the data to the database
        # This is the data that will be sent to the database
        # and used for commands, interlocks and control conditions
        # Also to identify the robot and its type
        Datalog.connect_to_mssql(log_Data)
        
        # ##########################################

       # Check the difference in Ultrasonic sensor readings

        # Arduino_ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0', baud, timeout=5) 

        # def ConfinementHandler():
        #     Arduino_ser.write(b'S')  # Send 'S' to the Arduino
        #     time.sleep(2)
        #     Arduino_ser.write(b'B')
        #     time.sleep(2)
        #     Arduino_ser.write(b'A')


        try:
            current_time = time.time()
            reading_difference = 0
            time_difference = 0
            if not hasattr(self, 'last_ultrasonic_reading'):
                self.last_ultrasonic_reading = self.ULTRASENSOR_DIST
                self.last_reading_time = current_time

                reading_difference = abs(float(self.ULTRASENSOR_DIST) - float(self.last_ultrasonic_reading))
                time_difference = current_time - self.last_reading_time

            if reading_difference < 5 and time_difference <= 5:
                self.get_logger().info('Ultrasonic sensor reading difference is less than 5 in the last 5 seconds.')
                # ConfinementHandler()

            # Update the last reading and time
            self.last_ultrasonic_reading = float(dist_)
            self.last_reading_time = current_time

        except ValueError:
            self.get_logger().error('Error: Invalid ultrasonic sensor reading.')


        print("enc_L : ", ENC_TOTAL_COUNT_L, '|', end = ' ')
        print("enc_R : ", ENC_TOTAL_COUNT_R, '|', end = ' ')
        print("count_L : ", COUNTER_L, '|', end = ' ')
        print("count_R : ", COUNTER_R, '|', end = ' ')
        print("rotation1 : ", rotation1, '|', end = ' ')
        print("rotation2 : ", rotation2)

        print("UltraSensor Distance : ", dist_, '|', end = ' ')
        print("Yaw : ", esp_values[1], '|', end = ' ')
        print("Pitch : ", esp_values[2], '|', end = ' ')
        print("Roll : ", esp_values[3])

        print(esp_values)
        return esp_values

        
#########################################################
######################## Logs ###########################
Routine_Message = rclpy.logging.get_logger('ROUTINE MESSAGE')
Arduino_Logs = rclpy.logging.get_logger('ARDUIO LOGS')
ESP32_Logs = rclpy.logging.get_logger('ESP32 LOGS')
Odometry_logs = rclpy.logging.get_logger('ODOMETRY LOGS')
#########################################################



def main(args=None):
    
    Routine_Message.info(' Initialising ROS2 Node. Please Wait')
  
    time.sleep(2)
    Routine_Message.info('Starting Serial Comms to ESP32 Node. Initialisation in Progress')

    write_data()
    time.sleep(10)
    Routine_Message.info('Starting ROS2 Node')

    rclpy.init(args=args)
    time.sleep(10)
    Routine_Message.info('Emptying Wrong Buffer Data from ESP32')

    Routine_Message.info('Please wait While ROS Node starts')
    node = DataSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    

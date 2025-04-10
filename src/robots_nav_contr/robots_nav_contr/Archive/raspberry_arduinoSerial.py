#!/usr/bin/env python3

# This code has been replaced by octavia_rosdata
# This can still be used but serial data transfer hasnt been perfected as 
# is in octavia_rosdata


import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

import serial
import time



# robots_nav_contr
global command
global sensorsdetails


#ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0', 9600, timeout=5)

class AutoCommandReceiver(Node):
    def __init__(self):
        super().__init__("octavia_command_receiver")
        self.get_logger().info("...Node initiated. Robot # Listening to robot_auto_command Node...")
        self.receiver_ = self.create_subscription(String, '/auto_command', self.receiver_callback, 10) # Message type to receive, name of the topic to subscribe to and the buffer size
        self.ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0', 9600, timeout=5) #  Corresponding to /ttyUSB0
        
        self.publisher = self.create_publisher(String, '/arduino_dat', 10)  # Publishes to another topic
        
    def receiver_callback(self, msg):
        self.get_logger().info(f"Received: {msg.data}")
        command = msg.data

        # Forward the received message to the publisher
        
        print('Message to Send is : ' , command)
        self.ser.write(bytes(command.encode("utf-8")))
        sent_command = str(bytes(command.encode("utf-8")))
        print('Message Sent is:  ', sent_command)

        ########################################################
        # READ FROM ARDUINO
        #######################################################

        input_str = self.ser.readline()
        decoded_input_str = input_str.decode("utf-8").strip()
        encoderData = decoded_input_str.split(",")

        datato_pub = String()
        datato_pub.data = decoded_input_str
        self.publisher.publish(datato_pub)            
        
        #######################################################

        ########################################################
        # WRITE STATUS BACK TO ARDUINO
        ########################################################
        
        input_str = self.ser.readline().decode("utf-8").strip()
        if (input_str ==""):
                print(".")
        else:
                # read response back from Arduino
                print ("Read input back: " + input_str)
        ########################################################
        return encoderData

    def receiver_callback2():
        input_str = serial.Serial.readline()
        decoded_input_str = input_str.decode("utf-8").strip()
        encoderData = decoded_input_str.split(",")
        return encoderData
    
def main(args=None):
    # Initialise ROS2 constroctor
    rclpy.init(args=args)
    # Create Node
    node = AutoCommandReceiver()
    # Use the Node
    rclpy.spin(node) # Runs the node continuously
    #Destroy/Shutdown Node
    rclpy.shutdown()

if __name__== '__main__':
    main()

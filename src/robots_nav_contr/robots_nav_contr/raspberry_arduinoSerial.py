#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time

# robots_nav_contr
global command


#ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-port0', 9600, timeout=5)

class AutoCommandReceiver(Node):
    def __init__(self):
        super().__init__("robot_command_receiver")
        self.get_logger().info("...Node initiated. Robot # Listening to robot_auto_command Node...")
        self.receiver_ = self.create_subscription(String, '/auto_command', self.receiver_callback, 10) # Message type to receive, name of the topic to subscribe to and the buffer size
        self.ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-port0', 9600, timeout=5)
        
    def receiver_callback(self, msg):
        self.get_logger().info(f"Received {msg.data}")
        command = msg.data
        print('Message to Send is : ' , command)
        self.ser.write(bytes(command.encode("utf-8")))
        sent_command = str(bytes(command.encode("utf-8")))
        

        print('Message Sent is:  ', sent_command)

        # ######################################################
        # read from Arduino
        input_str = self.ser.readline()
        print(input_str)
        print ("Read input " + input_str.decode("utf-8").strip() + " from Arduino")

        # ######################################################
        # write status back
        
        input_str = self.ser.readline().decode("utf-8").strip()
        if (input_str ==""):
                print(".")
        else:
                # read response back from Arduino
                print ("Read input back: " + input_str)
        # ####################################################################

    def receiver_callback2(self, msg):
        self.get_logger().info('Received: "%s"' % msg.data)
        self.ser.write(msg.data.encode())  # Send data to Arduino
        print(msg.data.encode())

    
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

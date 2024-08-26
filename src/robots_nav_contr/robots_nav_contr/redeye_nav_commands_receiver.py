#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from robots_nav_contr import move
from robots_nav_contr import encoders
import time
import RPi.GPIO as GPIO
from robots_nav_contr import ultra

# robots_nav_contr


class AutoCommandReceiver(Node):
    

    def __init__(self):
        super().__init__("redeye_command_receiver")
        self.get_logger().info("...Node initiated. Redeye Listening to robot_auto_command Node...")
        self.receiver_ = self.create_subscription(String, '/auto_command', self.receiver_callback, 10) # Message type to receive, name of the topic to subscribe to and the buffer size

        self.count = 0
        self.controlFlag = False

    def receiver_callback(self, msg: String):
        self.get_logger().info(f"Received {msg.data}")
        command = msg.data

        move.setup()
        match command:
            case "hi":
                print("Hello, How are you today ROS2?.")
            case "Ready":
                print("Cool.")
            case "":
                print("Say again Please")

            case "F":
                print("Okay, Program started")
                
                move.move(100, 'backward', 'no', 1)
                encoders.wheelEncodersReading()
                pass

            case "S":
                move.motorStop()
                print("Okay, Program stopped.")
                pass

            case _:
                print("The language doesn't matter; what matters is solving problems.")





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
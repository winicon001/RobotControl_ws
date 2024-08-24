#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import move
import encoders
import time
import RPi.GPIO as GPIO
import ultra

# robots_nav_contr

class AutoCommandReceiver(Node):
    def __init__(self):
        super().__init__("redeye_command_receiver")
        self.get_logger().info("...Node initiated. Redeye Listening to robot_auto_command Node...")
        self.receiver_ = self.create_subscription(String, '/auto_command', self.receiver_callback, 10) # Message type to receive, name of the topic to subscribe to and the buffer size

        self.count = 0

    def receiver_callback(self, msg: String):
        self.get_logger().info(f"Received {msg.data}")
        command = msg.data

        match command:
            case "hi":
                print("Hello, How are you today ROS2?.")
            case "Ready":
                print("Cool.")
            case "":
                print("Say again Please")

            case "start":
                print("Okay, Program started")
                move.setup()
                move.move(100, 'forward', 'no', 1)
                encoders.wheelEncodersReading()

            case "stop":
                # move.motorStop()
                move.move(0, 'forward', 'no', 1)
                print("Okay, Program stopped.")

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
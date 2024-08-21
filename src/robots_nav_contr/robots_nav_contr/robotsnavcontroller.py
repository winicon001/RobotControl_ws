#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# robots_nav_contr

class AutoCommand(Node):
    def __init__(self):
        super().__init__("robot_auto_command")
        self.get_logger().info("...Automatic Swarm Robot Controller Initialising...")
        self.publishers_ = self.create_publisher(String, 'auto_command', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.command_callback)

        self.count = 0

    def command_callback(self):

        msg =String()

        # Create the characters interface for commands input
        msg.data = input("Enter the command:  ")
        # Publish the comadnd
        self.publishers_.publish(msg)
        self.get_logger().info(f"Publishing {msg}")

def main(args=None):
    # Initialise ROS2 constroctor
    rclpy.init(args=args)
    # Create Node
    node = AutoCommand()
    # Use the Node
    rclpy.spin(node) # Runs the node continuously

    #Destroy/Shutdown Node
    rclpy.shutdown()

if __name__== '__main__':
    main()
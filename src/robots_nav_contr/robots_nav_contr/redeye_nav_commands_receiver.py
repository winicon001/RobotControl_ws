#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# robots_nav_contr

class AutoCommandReceiver(Node):
    def __init__(self):
        super().__init__("redeye_command_receiver")
        self.get_logger().info("...Node initiated. Robot # Listening to robot_auto_command Node...")
        self.receiver_ = self.create_subscription(String, '/auto_command', self.receiver_callback, 10) # Message type to receive, name of the topic to subscribe to and the buffer size

        self.count = 0

    def receiver_callback(self, msg: String):
        self.get_logger().info(f"Received {msg.data}")


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
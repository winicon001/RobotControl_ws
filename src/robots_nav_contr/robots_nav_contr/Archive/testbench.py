#!/usr/bin/env python3

import time
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

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
        # Process the data received
        self.get_logger().info(f'Received final data: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = DataSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

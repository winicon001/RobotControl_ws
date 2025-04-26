#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from robots_nav_contr import move
from robots_nav_contr import encoders
import time
import RPi.GPIO as GPIO
from robots_nav_contr import ultra
from robots_nav_contr import MainRoutine
import threading


# robots_nav_contr
speed = 0

class AutoCommandReceiver(Node):
    
    def __init__(self):
        super().__init__("redeye_command_receiver")
        self.get_logger().info("...Node initiated. Redeye Listening to robot_auto_command Node...")
        self.receiver_ = self.create_subscription(String, '/auto_command', self.receiver_callback, 10) # Message type to receive, name of the topic to subscribe to and the buffer size

        self.count = 0
        self.controlFlag = False
        self.last_command = None

        self.publisher = self.create_publisher(String, '/redEye_Arduino_data', 10)  # Publishes to another topic

    def continuous_movement(self):
        print("...Continuous Movement and Data Gathering Initiated...")
        while self.controlFlag:
            MainRoutine.robotmainroutine()
            
            enc1, enc1Total, Rev_L, dist_L = encoders.enc()
            time.sleep(0.1)

            # Allow ROS to process new messages
            rclpy.spin_once(self, timeout_sec=0.1)

            if not self.controlFlag:
                print("Exiting Continuous Movement and Data Gathering.")
                break

    def receiver_callback(self, msg: String):
        self.get_logger().info(f"Received {msg.data}")
        command = msg.data

        # Simulated Message from Arduino - Arduino not used in RedEye Robot
        arduino_msg = String()
        arduino_msg.data = "Hello Everyone, I am here if you need me for Arduino Interface"
        self.publisher.publish(arduino_msg)

        def continuous_movement(self):
            print("...Continuous Movement and Data Gathering Initiated...")
            while self.controlFlag:
                MainRoutine.robotmainroutine()
                
                # enc1, enc1Total, Rev_L, dist_L = encoders.enc()
                time.sleep(0.1)

                # Allow ROS to process new messages
                rclpy.spin_once(self, timeout_sec=0.1)

                if not self.controlFlag:
                    print("Exiting Continuous Movement and Data Gathering.")
                    pass
 

        move.setup()
        match command:
            case "hi":
                print("Hello, How are you today ROS2?.")
            case "Ready":
                print("Cool.")
            case "":
                print("Say again Please")

            case "M":
                print("...Main Routine Initiated...")
                MainRoutine.robotmainroutine()
                pass

            case "F":
                print("...Continuous Movement and Data Gathering Initiated...")
                self.last_command = "F"
                self.controlFlag = True

                # Start a new thread for continuous execution
                movement_thread = threading.Thread(target=continuous_movement, args=(self,))
                movement_thread.start()


            case "S":
                self.last_command = "S"
                self.controlFlag = False
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
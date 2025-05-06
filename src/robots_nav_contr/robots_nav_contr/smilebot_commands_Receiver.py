# This routine is the subscription routine for robot command received from the 
# general robots command topic /auto_command. 
# It also publishes the Data read on  Arduino serial port on /SmileBot_Arduino_data topic
# 


import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import threading
import time

class SerialHandler:
    def __init__(self, port, baudrate):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
        except serial.serialutil.SerialException as e:
            print(f"Error: {e}")
            self.ser = None

    def read_from_serial(self):
        if self.ser and self.ser.is_open:
            try:
                data = self.ser.readline().decode('utf-8').strip()
                return data
            except serial.serialutil.SerialException as e:
                print(f"Serial read error: {e}")
                return None
            except UnicodeDecodeError:
                print("Error decoding serial data.")
                return None # Handle invalid characters
        else:
            print("Serial port is not open or available.")
            return None

    def send_to_serial(self, data):
        """Send data to the serial port."""
        if self.ser.is_open:
            self.ser.write(data.encode('utf-8'))

Arduino_Logs = rclpy.logging.get_logger('ARDUIO LOGS')

class ROS2SerialNode(Node):
    def __init__(self, serial_port, baudrate):
        """Initialize the ROS2 node and serial handler."""
        super().__init__('smilebot_command_receiver')

        # Set up the serial handler
        self.serial_handler = SerialHandler(serial_port, baudrate)

        # ROS2 subscription
        self.subscription = self.create_subscription(
            String,
            '/auto_command',  # Replace with your topic name
            self.listener_callback,
            10
        )

        self.publisher = self.create_publisher(String, '/SmileBot_Arduino_data', 10)  # Publishes to another topic


        # Thread for continuous reading from the serial port
        self.stop_thread = False
        self.serial_thread = threading.Thread(target=self.read_serial_data)
        self.serial_thread.start()

        # Storage for serial data to use elsewhere
        self.serial_data = None

    def listener_callback(self, msg):
        """Callback for the ROS2 subscriber."""
        self.get_logger().info(f"Received from ROS topic: {msg.data}")
        self.serial_handler.send_to_serial(msg.data)  # Send the data to the serial port

    def read_serial_data(self):
        """Read from the serial port and store the data."""
        while not self.stop_thread:
            try:
                # Read data from the serial port
                data = self.serial_handler.read_from_serial()
                if data:
                    # self.get_logger().info(f"Received from Serial: {data}")
                    self.serial_data = data  # Store the data for use elsewhere in the project
            except serial.serialutil.SerialException:
                Arduino_Logs.info("Serial port not available. Retrying...")
                time.sleep(1)  # Wait before retrying

    def use_serial_data(self):
        """Use the stored serial data elsewhere in the project."""
        if self.serial_data:
            self.get_logger().info(f"Using Serial Data: {self.serial_data}")
            # Add your logic here to process or use the data

            #############################################
            #########DATA TO ARDUINO_DATA SUBSCRIBER NODE
            datato_pub = String()
            datato_pub.data = self.serial_data
            self.publisher.publish(datato_pub)    
            #############################################

    def destroy_node(self):
        """Stop the serial thread and destroy the node."""
        self.stop_thread = True
        self.serial_thread.join()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    # Replace with your serial port (e.g., '/dev/ttyUSB0' or 'COM3') and baudrate
    node = ROS2SerialNode(serial_port='/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-port0', baudrate=9600)

    try:
        # Periodically use serial data elsewhere in the project
        timer = node.create_timer(1.0, node.use_serial_data)  # Call every 1 second
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
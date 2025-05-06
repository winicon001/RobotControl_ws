import math
# from octavia_MainRoutine import DataSubscriber
import rclpy

# rclpy.init()


class DifferentialDriveOdometry:
    def __init__(self, wheel_radius, wheel_base):
        self.wheel_radius = wheel_radius
        self.wheel_base = wheel_base
        self.x = 0.0  # Robot's X position
        self.y = 0.0  # Robot's Y position
        self.theta = 0.0  # Robot's orientation

    def update(self, left_wheel_speed, right_wheel_speed, dt):
        v_left = left_wheel_speed * self.wheel_radius
        v_right = right_wheel_speed * self.wheel_radius

        v_center = (v_left + v_right) / 2.0
        omega = (v_right - v_left) / self.wheel_base

        delta_theta = omega * dt
        delta_x = v_center * math.cos(self.theta) * dt
        delta_y = v_center * math.sin(self.theta) * dt

        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta

        return self.x, self.y, self.theta

OdometryMessage = rclpy.logging.get_logger('ODOMETRY MESSAGE')


def MainRoutine(wheel_radius, wheel_base, left_wheel_speed, right_wheel_speed, dt):
    OdometryMessage.info("Starting Differential Drive Odometry Calculation")
    # Initialize the odometry with wheel radius and wheel base
    # wheel_radius = 0.1 m, wheel_base = 0.5 m
    # Replace these values with actual wheel speeds and time delta
    wheel_radius = 0.1  # meters
    wheel_base = 0.5  # meters
    # left_wheel_speed = 2.0  # m/s
    # right_wheel_speed = 2.5  # m/s
    dt = 0.1  # seconds
    odometry = DifferentialDriveOdometry(wheel_radius=0.1, wheel_base=0.5)
    x, y, theta = odometry.update(left_wheel_speed, right_wheel_speed, 0.1)
    # Print the updated position and orientation
    OdometryMessage.info(f"Updated Position: ({x:.2f}, {y:.2f}), Orientation: {theta:.2f} rad")
    return x, y, theta

# Odometry Calculation 
if __name__ == "__main__":
    MainRoutine()


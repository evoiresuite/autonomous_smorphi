import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial

class SmorphiDriver(Node):
    def __init__(self):
        super().__init__('smorphi_driver')

        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

    def cmd_callback(self, msg: Twist):
        vx = msg.linear.x
        wz = msg.angular.z

        data = f"{vx},{wz}\n"
        self.ser.write(data.encode())

        self.get_logger().info(f'Sent to ESP32: {data.strip()}')

def main(args=None):
    rclpy.init(args=args)
    node = SmorphiDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

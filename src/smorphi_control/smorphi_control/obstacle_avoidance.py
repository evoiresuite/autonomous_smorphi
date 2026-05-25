import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')
        self.sub = self.create_subscription(
            LaserScan,
            '/front_obstacle_scan',
            self.scan_callback,
            10
        )
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def scan_callback(self, msg):
        cmd = Twist()

        valid_ranges = [
            r for r in msg.ranges
            if not math.isinf(r) and not math.isnan(r)
]
        distance = min(valid_ranges) if valid_ranges else float('inf')

        if distance > 0.25:
            cmd.linear.x = 0.1
            cmd.angular.z = 0.0
            self.get_logger().info('AMAN: maju')
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
            self.get_logger().info(f'OBSTACLE {distance:.2f} m: belok')

        self.pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

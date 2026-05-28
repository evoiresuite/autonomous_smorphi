import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math


class LineFollowing(Node):
    def __init__(self):
        super().__init__('line_following_node')

        self.left = float('inf')
        self.center = float('inf')
        self.right = float('inf')

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_subscription(LaserScan, '/line_left_scan', self.left_cb, 10)
        self.create_subscription(LaserScan, '/line_center_scan', self.center_cb, 10)
        self.create_subscription(LaserScan, '/line_right_scan', self.right_cb, 10)

        self.timer = self.create_timer(0.1, self.control_loop)

        self.last_error = 0.0

    def get_range(self, msg):
        if not msg.ranges:
            return float('inf')
        r = msg.ranges[0]
        if math.isnan(r):
            return float('inf')
        return r

    def left_cb(self, msg):
        self.left = self.get_range(msg)

    def center_cb(self, msg):
        self.center = self.get_range(msg)

    def right_cb(self, msg):
        self.right = self.get_range(msg)

    def control_loop(self):
        cmd = Twist()

        threshold = 0.05

        l = self.left < threshold
        c = self.center < threshold
        r = self.right < threshold

        if l or c or r:
            weights = []
            if l:
                weights.append(-1.0)
            if c:
                weights.append(0.0)
            if r:
                weights.append(1.0)

            error = sum(weights) / len(weights)
            self.last_error = error

            base_speed = 0.05
            kp = 0.12

            cmd.linear.x = base_speed
            cmd.angular.z = -kp * error

            status = f'FOLLOW | error={error:.2f}'

        else:
            cmd.linear.x = 0.02
            cmd.angular.z = -0.08 * self.last_error
            status = f'LOST | last_error={self.last_error:.2f}'

        self.pub.publish(cmd)

        self.get_logger().info(
            f'{status} | L={self.left:.3f} C={self.center:.3f} R={self.right:.3f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = LineFollowing()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math


# ===== Kalibrasi Sensor =====
BASELINE = 0.0899      # Jarak sensor ke lantai tanpa garis
LINE_HEIGHT = 0.005    # Perbedaan tinggi karena garis
THRESHOLD = BASELINE - (LINE_HEIGHT / 2)   # ≈ 0.0874

class LineFollowing(Node):
    def __init__(self):
        super().__init__('line_following_node')

        self.left = float('inf')
        self.right = float('inf')

        self.pub = self.create_publisher(Twist, '/line_cmd', 10)

        self.create_subscription(LaserScan, '/line_left_scan', self.left_cb, 10)
        self.create_subscription(LaserScan, '/line_right_scan', self.right_cb, 10)

        self.timer = self.create_timer(0.1, self.control_loop)

    def get_range(self, msg):
        if not msg.ranges:
            return float('inf')
        r = msg.ranges[0]
        if math.isnan(r):
            return float('inf')
        return r

    def left_cb(self, msg):
        self.left = self.get_range(msg)

    def right_cb(self, msg):
        self.right = self.get_range(msg)

    def control_loop(self):
        cmd = Twist()

        threshold = THRESHOLD

        left_status = 0 if self.left < THRESHOLD else 1
        right_status = 0 if self.right < THRESHOLD else 1

        if right_status == 1 and left_status == 0:
            cmd.linear.x = 0.03
            cmd.angular.z = 0.25
            status = "TURN LEFT"

        elif right_status == 0 and left_status == 1:
            cmd.linear.x = 0.03
            cmd.angular.z = -0.25
            status = "TURN RIGHT"

        elif right_status == 0 and left_status == 0:
            cmd.linear.x = 0.06
            cmd.angular.z = 0.0
            status = "FORWARD"

        else:
            cmd.linear.x = 0.0
            cmd.angular.z = -0.25
            status = "SEARCH LINE"

        self.pub.publish(cmd)

        self.get_logger().info(
            f'{status} | L={self.left:.3f} R={self.right:.3f} '
            f'| LS={left_status} RS={right_status}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = LineFollowing()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

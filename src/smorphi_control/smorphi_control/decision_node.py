import rclpy

from rclpy.node import Node

from geometry_msgs.msg import Twist

from sensor_msgs.msg import LaserScan

import math


class DecisionNode(Node):

    def __init__(self):

        super().__init__('decision_node')

        self.line_cmd = Twist()
        self.obstacle_cmd = Twist()

        self.obstacle_distance = float('inf')

        self.create_subscription(
            Twist,
            '/line_cmd',
            self.line_callback,
            10)

        self.create_subscription(
            Twist,
            '/obstacle_cmd',
            self.obstacle_callback,
            10)

        self.create_subscription(
            LaserScan,
            '/front_obstacle_scan',
            self.scan_callback,
            10)

        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.timer = self.create_timer(
            0.05,
            self.control_loop)

    def line_callback(self,msg):

        self.line_cmd = msg

    def obstacle_callback(self,msg):

        self.obstacle_cmd = msg

    def scan_callback(self,msg):

        valid = [

            r for r in msg.ranges

            if not math.isinf(r)
            and not math.isnan(r)

        ]

        if valid:

            self.obstacle_distance = min(valid)

        else:

            self.obstacle_distance = float('inf')

    def control_loop(self):

        if self.obstacle_distance < 0.35:

            self.pub.publish(self.obstacle_cmd)

            self.get_logger().info("MODE : OBSTACLE")

        else:

            self.pub.publish(self.line_cmd)

            self.get_logger().info("MODE : LINE")


def main(args=None):

    rclpy.init(args=args)

    node = DecisionNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

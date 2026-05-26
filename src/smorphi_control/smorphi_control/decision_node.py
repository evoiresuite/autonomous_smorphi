import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Bool
from geometry_msgs.msg import Twist
import time

class DecisionNode(Node):
    def __init__(self):
        super().__init__('decision_node')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_subscription(Int32, '/line_pos', self.line_cb, 10)
        self.create_subscription(Bool, '/obstacle_detected', self.obstacle_cb, 10)

        self.line_pos = 99
        self.obstacle = False

        self.state = "FOLLOW"
        self.state_time = time.time()

        self.timer = self.create_timer(0.05, self.loop)

    def line_cb(self, msg):
        self.line_pos = msg.data

    def obstacle_cb(self, msg):
        self.obstacle = msg.data

    def set_state(self, s):
        self.state = s
        self.state_time = time.time()
        self.get_logger().info(f"STATE -> {s}")

    def update_state(self):
        now = time.time()

        if self.state == "FOLLOW":
            if self.obstacle:
                self.set_state("AVOID")
            elif self.line_pos == 99:
                self.set_state("SEARCH")

        elif self.state == "AVOID":
            if not self.obstacle and now - self.state_time > 1.0:
                self.set_state("RECOVERY")

        elif self.state == "RECOVERY":
            if self.line_pos != 99:
                self.set_state("FOLLOW")
            elif now - self.state_time > 2.0:
                self.set_state("SEARCH")

        elif self.state == "SEARCH":
            if self.line_pos != 99:
                self.set_state("FOLLOW")

    def loop(self):
        self.update_state()

        t = Twist()

        if self.state == "FOLLOW":
            t.linear.x = 0.25
            if self.line_pos == -1:
                t.angular.z = 0.7
            elif self.line_pos == 1:
                t.angular.z = -0.7

        elif self.state == "SEARCH":
            t.angular.z = 0.6

        elif self.state == "AVOID":
            t.linear.y = 0.35  # geser mekanum

        elif self.state == "RECOVERY":
            t.linear.x = 0.2

        self.cmd_pub.publish(t)

def main():
    rclpy.init()
    node = DecisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

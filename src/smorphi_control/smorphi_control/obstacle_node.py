import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import random
import time

class ObstacleNode(Node):
    def __init__(self):
        super().__init__('obstacle_node')

        self.pub = self.create_publisher(Bool, '/obstacle_detected', 10)
        self.timer = self.create_timer(0.5, self.publish_obstacle)

        # state awal
        self.obstacle_state = False
        self.state_end_time = time.time() + self.random_duration()

    def random_duration(self):
        # durasi antara 5–12 detik
        return random.randint(5, 12)

    def publish_obstacle(self):
        now = time.time()

        # kalau durasi state habis, ganti state
        if now >= self.state_end_time:
            self.obstacle_state = not self.obstacle_state
            self.state_end_time = now + self.random_duration()

        msg = Bool()
        msg.data = self.obstacle_state
        self.pub.publish(msg)

        self.get_logger().info(f'Obstacle: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

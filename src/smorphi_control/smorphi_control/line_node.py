import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class LineNode(Node):
    def __init__(self):
        super().__init__('line_node')

        self.pub = self.create_publisher(Int32, '/line_pos', 10)
        self.timer = self.create_timer(0.5, self.publish_line)

    def publish_line(self):
        msg = Int32()
        msg.data = 0   # simulasi selalu lihat garis
        self.pub.publish(msg)
        self.get_logger().info('Publishing: LINE POS 0')

def main(args=None):
    rclpy.init(args=args)
    node = LineNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

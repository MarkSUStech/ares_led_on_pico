import rclpy
from rclpy.node import Node

from led_control_interfaces.msg import LedSegment
from std_msgs.msg import Int32MultiArray

class SegmentBridge(Node):
    def __init__(self):
        super().__init__('segment_bridge')
        self.declare_parameter('led_count', 30)

        self.sub = self.create_subscription(
            LedSegment, 'segment_command', self.on_command, 10)

        self.pub = self.create_publisher(
            Int32MultiArray, '/ares/led/segment', 10)
        
    def on_command(self, msg: LedSegment):
        if msg.brightness > 100:
            self.get_logger().error('brightness must be in the range of [0, 100]')
            return

        k = msg.brightness / 100.0
        out = Int32MultiArray()
        out.data = [
            self.get_parameter('led_count').value,
            msg.left, msg.right,
            round(msg.r * k), round(msg.g * k), round(msg.b * k),
        ]
        self.pub.publish(out)
        
def main(args=None):
    rclpy.init(args=args)
    node = SegmentBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
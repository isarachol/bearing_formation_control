from math import sin, cos, pi
import threading
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion, Twist
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

# can try to modify this https://github.com/ros-teleop/teleop_twist_keyboard/blob/master/teleop_twist_keyboard.py
# Basically use Twist msg type to command velocity

class SingleStatePublisher(Node):

    def __init__(self):
        super().__init__('single_state_publisher')
        self.publisher_ = self.create_publisher(Twist, 'diff_cont/cmd_vel_unstamped', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        if self.i % 5 == 0:
            twist = Twist()
            twist.linear.x = 3.
            twist.linear.y = 0.
            twist.linear.z = 0.
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = 2.
            self.publisher_.publish(twist)
        self.i += 1
        self.get_logger().info('Publishing: message number "%d"' % self.i)


def main(args=None):
    rclpy.init(args=args)
    node = SingleStatePublisher()
    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


OLEK_EDASI_1 = 0
OLEK_POORDE_1 = 1
OLEK_EDASI_2 = 2
OLEK_POORDE_2 = 3
OLEK_VALMIS = 4


class Marsruut(Node):
    def __init__(self):
        super().__init__('marsruut')

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.olek = OLEK_EDASI_1

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.odom_ready = False

        self.start_x = None
        self.start_y = None
        self.start_yaw = None

        self.timer = self.create_timer(0.1, self.control_loop)

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        self.yaw = self.quaternion_to_yaw(q.x, q.y, q.z, q.w)

        if not self.odom_ready:
            self.start_new_step()

        self.odom_ready = True

    def quaternion_to_yaw(self, x, y, z, w):
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        return math.atan2(siny_cosp, cosy_cosp)

    def angle_diff(self, target, current):
        diff = target - current

        while diff > math.pi:
            diff -= 2.0 * math.pi

        while diff < -math.pi:
            diff += 2.0 * math.pi

        return diff

    def distance_from_start(self):
        dx = self.x - self.start_x
        dy = self.y - self.start_y
        return math.sqrt(dx * dx + dy * dy)

    def start_new_step(self):
        self.start_x = self.x
        self.start_y = self.y
        self.start_yaw = self.yaw

    def stop_robot(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.pub.publish(cmd)

    def control_loop(self):
        if not self.odom_ready:
            return

        cmd = Twist()

        if self.olek == OLEK_EDASI_1:
            if self.distance_from_start() < 1.0:
                cmd.linear.x = 0.20
                cmd.angular.z = 0.0
            else:
                self.stop_robot()
                self.olek = OLEK_POORDE_1
                self.start_new_step()
                return

        elif self.olek == OLEK_POORDE_1:
            target_yaw = self.start_yaw - math.pi / 2.0
            error = self.angle_diff(target_yaw, self.yaw)

            if abs(error) > 0.08:
                cmd.linear.x = 0.0
                cmd.angular.z = -0.45
            else:
                self.stop_robot()
                self.olek = OLEK_EDASI_2
                self.start_new_step()
                return

        elif self.olek == OLEK_EDASI_2:
            if self.distance_from_start() < 1.0:
                cmd.linear.x = 0.20
                cmd.angular.z = 0.0
            else:
                self.stop_robot()
                self.olek = OLEK_POORDE_2
                self.start_new_step()
                return

        elif self.olek == OLEK_POORDE_2:
            target_yaw = self.start_yaw - math.pi / 2.0
            error = self.angle_diff(target_yaw, self.yaw)

            if abs(error) > 0.08:
                cmd.linear.x = 0.0
                cmd.angular.z = -0.45
            else:
                self.stop_robot()
                self.olek = OLEK_VALMIS
                self.timer.cancel()
                return

        elif self.olek == OLEK_VALMIS:
            self.stop_robot()
            self.timer.cancel()
            return

        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = Marsruut()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.stop_robot()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

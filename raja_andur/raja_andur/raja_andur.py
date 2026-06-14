#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class RajaAndur(Node):
    def __init__(self):
        super().__init__('raja_andur')

        self.last_scan = None

        self.sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.timer = self.create_timer(1.0, self.print_table)

    def scan_callback(self, msg):
        self.last_scan = msg

    def sektori_min(self, ranges, center_index, width, default=8.0):
        n = len(ranges)
        values = []

        for i in range(center_index - width, center_index + width + 1):
            idx = i % n
            r = ranges[idx]

            if math.isfinite(r) and 0.12 < r < 8.0:
                values.append(r)

        if len(values) == 0:
            return default

        return min(values)

    def mark(self, distance):
        if distance < 0.5:
            return "[L\u00c4HEDAL]"
        if distance < 1.0:
            return "[HOIATUS]"
        return "[OK]"

    def print_table(self):
        if self.last_scan is None:
            return

        ranges = self.last_scan.ranges

        if len(ranges) < 720:
            return

        # Lidar index map:
        # ranges[180] = right
        # ranges[360] = front
        # ranges[540] = left

        vasak_sein = self.sektori_min(ranges, 540, 35)
        ette_vasak = self.sektori_min(ranges, 430, 35)
        otse_ette = self.sektori_min(ranges, 360, 35)
        ette_parem = self.sektori_min(ranges, 290, 35)
        parem_sein = self.sektori_min(ranges, 180, 35)

        print("=== Raja andurid ===")
        print(f"Vasak sein:    {vasak_sein:.2f} m  {self.mark(vasak_sein)}")
        print(f"Ette-vasak:    {ette_vasak:.2f} m  {self.mark(ette_vasak)}")
        print(f"Otse ette:     {otse_ette:.2f} m  {self.mark(otse_ette)}")
        print(f"Ette-parem:    {ette_parem:.2f} m  {self.mark(ette_parem)}")
        print(f"Parem sein:    {parem_sein:.2f} m  {self.mark(parem_sein)}")
        print("===================")


def main(args=None):
    rclpy.init(args=args)
    node = RajaAndur()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

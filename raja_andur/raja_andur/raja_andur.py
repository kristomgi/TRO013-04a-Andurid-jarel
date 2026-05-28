"""Moodul 04a, Ülesanne 1: Raja andur — lidar sektorite analüüs.

Ülesanne:
  Kirjuta sõlm, mis jagab lidari 360° vaate 5 sektoriks ja
  trükib iga sekundi tagant tabeli kaugustest.

Nõuded:
  - Subscribi /scan teemale
  - Jaga vaade 5 sektoriks: vasak sein, ette-vasak, otse ette, ette-parem, parem sein
  - Trüki tabel iga sekundi tagant
  - Märgista: [LÄHEDAL] < 0.5m, [HOIATUS] < 1.0m, [OK] >= 1.0m

Oodatav väljund:
  === Raja andurid ===
  Vasak sein:    0.45 m  [LÄHEDAL]
  Ette-vasak:    1.23 m  [OK]
  Otse ette:     2.87 m  [OK]
  Ette-parem:    1.15 m  [OK]
  Parem sein:    0.52 m  [LÄHEDAL]
  ===================

Käivita:
  Terminal 1: ros2 launch yahboom_webots webots.launch.py
  Terminal 2: ros2 run raja_andur raja_andur
"""
import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class RajaAndur(Node):

    def __init__(self):
        super().__init__('raja_andur')

        self.sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)

        # Trüki tabel 1× sekundis (mitte iga lidar sõnumiga)
        self.viimane_scan = None
        self.timer = self.create_timer(1.0, self.print_table)

        self.get_logger().info('Raja andur käivitatud!')

    def scan_callback(self, msg):
        self.viimane_scan = msg

    def sektori_min(self, ranges, algus, lopp, range_min, range_max):
        """Leia minimaalne kehtiv kaugus antud indeksvahemikus."""
        # TODO: filtreeri kehtivad mõõtmised (range_min <= r <= range_max, mitte inf/nan)
        # TODO: tagasta min() või inf kui ühtegi kehtivat pole
        #
        # Vihje:
        #   kehtivad = [ranges[i % len(ranges)] for i in range(algus, lopp)
        #               if range_min <= ranges[i % len(ranges)] <= range_max
        #               and not math.isinf(ranges[i % len(ranges)])]
        #   return min(kehtivad) if kehtivad else float('inf')
        return float('inf')  # TODO: asenda

    def print_table(self):
        if self.viimane_scan is None:
            return

        msg = self.viimane_scan
        ranges = msg.ranges

        # TODO: defineeri 5 sektori indeksid
        # Lidar indeksid (720 kiirt):
        #   ranges[360] = 0° = otse ette
        #   ranges[540] = 90° = vasak
        #   ranges[180] = -90° = parem
        #
        # Sektorid:
        #   Vasak sein:   indeksid 520-560 (~90° vasak ±20°)
        #   Ette-vasak:   indeksid 400-450 (~20-45° vasak)
        #   Otse ette:    indeksid 340-380 (±10° ette)
        #   Ette-parem:   indeksid 270-320 (~20-45° parem)
        #   Parem sein:   indeksid 160-200 (~90° parem ±20°)

        # TODO: arvuta iga sektori minimaalne kaugus
        # Vihje: kasuta self.sektori_min(ranges, algus, lopp, msg.range_min, msg.range_max)
        vasak_sein = float('inf')   # TODO
        ette_vasak = float('inf')   # TODO
        otse_ette = float('inf')    # TODO
        ette_parem = float('inf')   # TODO
        parem_sein = float('inf')   # TODO

        # TODO: trüki tabel
        # Vihje: kasuta self.margista(kaugus) et saada [LÄHEDAL]/[HOIATUS]/[OK]
        #
        # self.get_logger().info(
        #     f'\n=== Raja andurid ===\n'
        #     f'Vasak sein:    {vasak_sein:.2f} m  {self.margista(vasak_sein)}\n'
        #     f'Ette-vasak:    {ette_vasak:.2f} m  {self.margista(ette_vasak)}\n'
        #     f'Otse ette:     {otse_ette:.2f} m  {self.margista(otse_ette)}\n'
        #     f'Ette-parem:    {ette_parem:.2f} m  {self.margista(ette_parem)}\n'
        #     f'Parem sein:    {parem_sein:.2f} m  {self.margista(parem_sein)}\n'
        #     f'===================')

    def margista(self, kaugus):
        """Tagasta märgis kauguse põhjal."""
        if kaugus < 0.5:
            return '[LÄHEDAL]'
        elif kaugus < 1.0:
            return '[HOIATUS]'
        else:
            return '[OK]'


def main(args=None):
    rclpy.init(args=args)
    node = RajaAndur()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

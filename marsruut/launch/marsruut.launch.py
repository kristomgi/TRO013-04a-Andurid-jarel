"""Käivitusfail: Webots + marsruut.

Käivita: ros2 launch marsruut marsruut.launch.py
"""
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    webots_pkg = get_package_share_directory('yahboom_webots')

    webots_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(webots_pkg, 'launch', 'webots.launch.py')
        ),
    )

    marsruut_node = Node(
        package='marsruut',
        executable='marsruut',
        name='marsruut',
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription([
        webots_launch,
        marsruut_node,
    ])

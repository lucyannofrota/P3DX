from launch import LaunchDescription
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_context import LaunchContext

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

	launch_rviz = launch_ros.actions.Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=['-d' + 
		   PathJoinSubstitution([
				FindPackageShare('p3dx_bringup'),
				'rviz/p3dx.rviz'
			]).perform(LaunchContext())
		]
        )



	return LaunchDescription([
                launch_rviz
	])
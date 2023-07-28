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

	# URDF
	urdf_val = PathJoinSubstitution([
		FindPackageShare('p3dx_description_ros'),
		'urdf/pioneer3dx_fixed_joints.xml'
	]).perform(LaunchContext())

	print('Default urdf_file : {}'.format(urdf_val))

	urdf = LaunchConfiguration('urdf', default=urdf_val)

	declare_urdf_launch_arg = DeclareLaunchArgument(
		"urdf", default_value=urdf_val,
		description='URDF path [*.xml,*.urdf]'
	)

	# use_sim_time
	use_sim_time = LaunchConfiguration('use_sim_time', default='false')

	declare_use_sim_time_launch_arg = DeclareLaunchArgument(
		"use_sim_time", default_value='false',
		description='Use simulation clock'
	)

	# launch description
	launch_description = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			PathJoinSubstitution([
				FindPackageShare('p3dx_description_ros'),
				'launch/p3dx_description_ros2_launch.py'
			]).perform(LaunchContext())
		),
		launch_arguments={
		    'urdf': urdf,
			'use_sim_time': use_sim_time
		}.items(),
	)

	# launch_rviz = launch_ros.actions.Node(
    #     package="rviz2",
    #     executable="rviz2",
    #     name="rviz2",
    #     arguments=['-d' + 
	# 	   PathJoinSubstitution([
	# 			FindPackageShare('p3dx_bringup'),
	# 			'rviz/p3dx.rviz'
	# 		]).perform(LaunchContext())
	# 	]
    # )

	launch_nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('nav2_bringup'),
                'launch/navigation_launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )
	
	launch_slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('slam_toolbox'),
                'launch/online_async_launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': "/workspace/src/P3DX/p3dx_bringup/config/slam_toobox_config.yaml"
        }.items()
        # /workspace/src/P3DX/p3dx_bringup/config/slam_toobox_config.yamlle:=/workspace/src/P3DX/p3dx_bringup/config/slam
    )


	return LaunchDescription([
		declare_urdf_launch_arg,
		declare_use_sim_time_launch_arg,
		launch_description,
        launch_slam
        # launch_nav2,
        # launch_rviz,
	])
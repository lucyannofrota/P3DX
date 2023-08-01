from launch import LaunchDescription
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_context import LaunchContext
from launch.conditions import IfCondition

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

	# Get the launch directory
    bringup_dir = get_package_share_directory('nav2_bringup')
    launch_dir = os.path.join(bringup_dir, 'launch')

    # Create the launch configuration variables
    namespace = LaunchConfiguration('namespace')
    use_namespace = LaunchConfiguration('use_namespace')
    # slam = LaunchConfiguration('slam')
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = LaunchConfiguration('params_file')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    autostart = LaunchConfiguration('autostart')

    stdout_linebuf_envvar = SetEnvironmentVariable(
        'RCUTILS_LOGGING_BUFFERED_STREAM', '1')

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')

    # declare_use_namespace_cmd = DeclareLaunchArgument(
    #     'use_namespace',
    #     default_value='false',
    #     description='Whether to apply a namespace to the navigation stack')

    # declare_slam_cmd = DeclareLaunchArgument(
    #     'slam',
    #     default_value='False',
    #     description='Whether run a SLAM')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=PathJoinSubstitution([
				FindPackageShare('p3dx_bringup'),
				'params/p3dx_nav2.yaml'
			]).perform(LaunchContext()),
        description='Full path to the ROS2 parameters file to use for all launched nodes')

    declare_bt_xml_cmd = DeclareLaunchArgument(
        'default_bt_xml_filename',
        default_value=PathJoinSubstitution([
				FindPackageShare('nav2_bt_navigator'),
				'behavior_trees/navigate_w_replanning_and_recovery.xml'
			]).perform(LaunchContext()),
        description='Full path to the behavior tree xml file to use')

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', default_value='true',
        description='Automatically startup the nav2 stack')
    
    # # launch description
    # launch_description = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         PathJoinSubstitution([
    #             FindPackageShare('p3dx_description_ros'),
    #             'launch/p3dx_description_ros2_launch.py'
    #         ]).perform(LaunchContext())
    #     ),
    #     launch_arguments={
    #         'urdf': urdf,
    #         'use_sim_time': use_sim_time
    #     }.items(),
    # )

    # Specify the actions
    bringup_cmd_group = GroupAction([
        
        IncludeLaunchDescription(
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
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('slam_toolbox'),
                    'launch/online_async_launch.py'
                ])
            ]),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'params_file': params_file
                # "/workspace/src/P3DX/p3dx_bringup/config/slam_toobox_config.yaml"
            }.items()
            # /workspace/src/P3DX/p3dx_bringup/config/slam_toobox_config.yamlle:=/workspace/src/P3DX/p3dx_bringup/config/slam
        ),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([
        #         PathJoinSubstitution([
        #             FindPackageShare('slam_toolbox'),
        #             'launch/online_async_launch.py'
        #         ])
        #     ]),
        # # PythonLaunchDescriptionSource(os.path.join(launch_dir, 'slam_launch.py')),
        #     launch_arguments={'namespace': namespace,
        #                       'use_sim_time': use_sim_time,
        #                       'autostart': autostart,
        #                       'params_file': "/workspace/src/P3DX/p3dx_bringup/config/slam_toobox_config.yaml"}.items()),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, 'navigation_launch.py')),
            launch_arguments={'namespace': namespace,
                              'use_sim_time': use_sim_time,
                              'autostart': autostart,
                              'params_file': params_file,
                              'default_bt_xml_filename': default_bt_xml_filename,
                              'use_lifecycle_mgr': 'false',
                              'map_subscribe_transient_local': 'true'}.items()),
    ])

    return LaunchDescription([
        declare_urdf_launch_arg,
        # launch_description,
        stdout_linebuf_envvar,
        declare_namespace_cmd,
        # declare_use_namespace_cmd,
        # declare_slam_cmd,
        declare_use_sim_time_cmd,
        declare_params_file_cmd,
        declare_bt_xml_cmd,
        declare_autostart_cmd,
        # slam_launch,
        # nav2_launch,
        bringup_cmd_group
	])
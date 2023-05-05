from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_context import LaunchContext


def generate_launch_description():

    urdf = PathJoinSubstitution([
        FindPackageShare('p3dx_description_ros'),
        'urdf/pioneer3dx_fixed_joints.xml'
    ]).perform(LaunchContext())

    print('urdf_file : {}'.format(urdf))

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    declare_args = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[urdf]
    )

    return LaunchDescription([
        declare_args,
        state_publisher
    ])
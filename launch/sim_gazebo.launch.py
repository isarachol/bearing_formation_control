import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription #, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='bearing_formation_control' #<--- CHANGE ME

    x_sim = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','x_sim.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    # referenced from https://automaticaddison.com/how-to-load-a-world-file-into-gazebo-ros-2/
    # world_file_name = 'cans.world'
    # world_path = os.path.join(get_package_share_directory(package_name), 'worlds', world_file_name)

    # declare_world_cmd = DeclareLaunchArgument(name='world',
    #                     default_value=world_path,
    #                     description='Full path to the world model file to load')

    # params for higher gazebo response rate (frame rate)
    gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo.yaml')

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
             )
    # 'world': LaunchConfiguration('world')

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', '/robot_description',
                                   '-entity', 'my_bot',
                                   '-y', '0.5'],
                        output='screen')
    
    # spawn_entity2 = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                     arguments=['-topic', 'robot_description2',
    #                                '-entity', 'my_bot2',
    #                                '-x', '2.0'],
    #                     output='screen')

    # Run diff drive controller
    # diff_drive_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["diff_cont"],
    # )

    # diff_drive_spawner2 = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["diff_cont2"],
    # )

    # Run joint broad controller
    # joint_broad_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_broad"],
    # )

    # joint_broad_spawner2 = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_broad2"],
    # )

    # Launch them all!
    return LaunchDescription([
        x_sim,
        # declare_world_cmd,
        gazebo,
        spawn_entity,
        # spawn_entity2,
        # diff_drive_spawner,
        # diff_drive_spawner2,
        # joint_broad_spawner,
        # joint_broad_spawner2,
    ])

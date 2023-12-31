#!/usr/bin/python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,  ExecuteProcess, RegisterEventHandler
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.event_handlers import (OnProcessStart, OnProcessExit)
from launch_ros.descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
import random

# this is the function launch  system will look for
def generate_launch_description():
    ####### DATA INPUT ##########
    urdf_file = '/home/ananya/ros2_ws/src/my_box_bot_gazebo/urdf/Assem1_urdf.urdf'
    #xacro_file = "box_bot.xacro"robot_description
    package_description = "my_box_bot_gazebo"
    ####### DATA INPUT END ##########
    config = os.path.join( get_package_share_directory('my_box_bot_gazebo')
    )
    print("Fetching URDF ==>")
    robot_desc_path = os.path.join(get_package_share_directory(package_description), "urdf", urdf_file)
    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        emulate_tty=True,
        parameters=[{'use_sim_time': True, 'robot_description': ParameterValue(Command(['xacro ',robot_desc_path]), value_type=str)}],
        output="screen"
    )

    # Position and orientation
    # [X, Y, Z]
    position = [0.0, 0.0, 0.0]
    # [Roll, Pitch, Yaw]
    orientation = [0.0, 0.0, 0.0]
    # Base Name or robot
    robot_base_name = "quadruped"
    # Spawn ROBOT Set Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=['-entity', robot_base_name,
                    '-x', str(position[0]), '-y', str(position[1]
                                                        ), '-z', str(position[2]),
                    '-R', str(orientation[0]), '-P', str(orientation[1]
                                                        ), '-Y', str(orientation[2]),
                    '-topic', '/robot_description'
                    ]
    )

    # create and return launch description object
    return LaunchDescription([  
        robot_state_publisher_node,
        spawn_robot
    ])
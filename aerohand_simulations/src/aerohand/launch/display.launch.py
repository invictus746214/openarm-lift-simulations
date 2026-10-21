# Copyright 2025 Chestnut Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    package_path = Path(get_package_share_directory("aerohand"))

    left_model = DeclareLaunchArgument(
        "model",
        default_value=str(package_path / "urdf" / "aero_hand_open_left.urdf"),
        description="Absolute path to the left-hand URDF",
    )
    right_model = DeclareLaunchArgument(
        "right_model",
        default_value=str(package_path / "urdf" / "aero_hand_open_right.urdf"),
        description="Absolute path to the right-hand URDF",
    )
    gui = DeclareLaunchArgument(
        "gui",
        default_value="true",
        choices=["true", "false"],
        description="Enable joint_state_publisher_gui",
    )
    rviz_config = DeclareLaunchArgument(
        "rvizconfig",
        default_value=str(package_path / "rviz" / "config.rviz"),
        description="Absolute path to the RViz configuration",
    )
    software_rendering = DeclareLaunchArgument(
        "use_software_rendering",
        default_value="false",
        choices=["true", "false"],
        description="Use Mesa software rendering in RViz",
    )

    left_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]), value_type=str
    )
    right_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("right_model")]), value_type=str
    )

    nodes = [
        Node(
            namespace="left",
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": left_description}],
        ),
        Node(
            namespace="right",
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": right_description}],
        ),
        Node(
            namespace="left",
            package="joint_state_publisher",
            executable="joint_state_publisher",
            parameters=[{"robot_description": left_description}],
            condition=UnlessCondition(LaunchConfiguration("gui")),
        ),
        Node(
            namespace="left",
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            parameters=[{"robot_description": left_description}],
            condition=IfCondition(LaunchConfiguration("gui")),
        ),
        Node(
            namespace="right",
            package="joint_state_publisher",
            executable="joint_state_publisher",
            parameters=[{"robot_description": right_description}],
            condition=UnlessCondition(LaunchConfiguration("gui")),
        ),
        Node(
            namespace="right",
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            parameters=[{"robot_description": right_description}],
            condition=IfCondition(LaunchConfiguration("gui")),
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            output="screen",
            arguments=["-d", LaunchConfiguration("rvizconfig")],
            condition=UnlessCondition(LaunchConfiguration("use_software_rendering")),
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            output="screen",
            arguments=["--opengl", "210", "-d", LaunchConfiguration("rvizconfig")],
            env={"LIBGL_ALWAYS_SOFTWARE": "1", "QT_XCB_GL_INTEGRATION": "none"},
            condition=IfCondition(LaunchConfiguration("use_software_rendering")),
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="left_world_tf",
            arguments=["-0.10", "0", "0", "0", "0", "0", "world", "left_base_link"],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="right_world_tf",
            arguments=["0.10", "0", "0", "0", "0", "0", "world", "right_base_link"],
        ),
    ]

    return LaunchDescription(
        [left_model, right_model, gui, rviz_config, software_rendering, *nodes]
    )

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    package = Path(get_package_share_directory("aerohand_openarm_2_0"))
    model = package / "urdf" / "openarm_v20_aero_hands.urdf.xacro"
    robot_description = xacro.process_file(str(model)).toxml()

    return LaunchDescription(
        [
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[{"robot_description": robot_description}],
                output="screen",
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                parameters=[{"robot_description": robot_description}],
                output="screen",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", str(package / "rviz" / "combined.rviz")],
                output="screen",
            ),
        ]
    )

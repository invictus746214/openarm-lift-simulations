from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

from aerohand_openarm_1_0.urdf_filter import remove_link_visuals


def generate_launch_description():
    package = Path(get_package_share_directory("aerohand_openarm_1_0"))
    model = package / "urdf" / "openarm_v11_aero_hands.urdf.xacro"
    robot_description = xacro.process_file(str(model)).toxml()
    # The revised OpenArm v1.1 CAD export hides the two terminal J8 motor
    # housings. Keep link7 as the kinematic mounting frame, but omit its
    # visual geometry so the RViz preview matches that assembly state.
    robot_description = remove_link_visuals(
        robot_description,
        {"openarm_left_link7", "openarm_right_link7"},
    )

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

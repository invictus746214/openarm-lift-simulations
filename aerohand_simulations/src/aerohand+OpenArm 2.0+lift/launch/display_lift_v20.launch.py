from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

from aerohand_openarm_2_0_lift.urdf_filter import remove_link_visuals


def generate_launch_description():
    package = Path(get_package_share_directory("aerohand_openarm_2_0_lift"))
    model = package / "urdf" / "hei_lift_openarm_v20_aero_hands.urdf.xacro"
    robot_description = xacro.process_file(str(model)).toxml()
    # The official body mesh contains its own tall pedestal.  The supplied
    # combined STEP replaces that pedestal with the HEI lift and 60 mm moving
    # adapter, so keep the body frame but hide only its duplicate visual.
    robot_description = remove_link_visuals(
        robot_description,
        {"openarm_body_link0"},
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
                parameters=[
                    {
                        "robot_description": robot_description,
                        "zeros": {
                            "lift_joint": 0.0,
                        },
                    }
                ],
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

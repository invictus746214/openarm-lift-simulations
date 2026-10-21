from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    share = Path(get_package_share_directory("total_lift_openarm_sim"))
    urdf = share / "urdf" / "total_lift_openarm.urdf"
    rviz = share / "rviz" / "total_lift_openarm.rviz"
    description = urdf.read_text(encoding="utf-8")
    gui_model = ET.fromstring(description)
    solver_joints = {
        f"openarm_{side}_gripper_{part}_joint"
        for side in ("left", "right")
        for part in ("rotor", "link_positive", "link_negative")
    }
    for joint in list(gui_model.findall("joint")):
        if joint.get("name") in solver_joints:
            gui_model.remove(joint)
    gui_description = ET.tostring(gui_model, encoding="unicode")
    gui_urdf = Path(tempfile.gettempdir()) / "total_lift_openarm_gui.urdf"
    gui_urdf.write_text(gui_description, encoding="utf-8")
    return LaunchDescription([
        Node(package="robot_state_publisher", executable="robot_state_publisher", parameters=[{"robot_description": description}], output="screen"),
        Node(package="joint_state_publisher_gui", executable="joint_state_publisher_gui", arguments=[str(gui_urdf)], remappings=[("robot_description", "/total_lift_openarm_sim/gui_description_unused"), ("joint_states", "gui_joint_states")], output="screen"),
        Node(package="total_lift_openarm_sim", executable="gripper_linkage_kinematics", output="screen"),
        Node(package="rviz2", executable="rviz2", arguments=["-d", str(rviz)], output="screen"),
    ])

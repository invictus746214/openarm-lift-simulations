#!/usr/bin/env python3
"""Resolve the STEP-measured closed gripper linkage for robot_state_publisher."""

from __future__ import annotations

import math


# Pivot centers measured from the STEP cylindrical faces, in each gripper EE frame (mm).
ROTOR_PIN_POSITIVE = (-27.824, 28.737)
SLIDER_PIN_POSITIVE = (-18.600, 62.500)
ROTOR_PIN_NEGATIVE = (-ROTOR_PIN_POSITIVE[0], -ROTOR_PIN_POSITIVE[1])
SLIDER_PIN_NEGATIVE = (-SLIDER_PIN_POSITIVE[0], -SLIDER_PIN_POSITIVE[1])
PIN_RADIUS = math.hypot(*ROTOR_PIN_POSITIVE)
LINK_LENGTH = math.hypot(
    SLIDER_PIN_POSITIVE[0] - ROTOR_PIN_POSITIVE[0],
    SLIDER_PIN_POSITIVE[1] - ROTOR_PIN_POSITIVE[1],
)
MIN_SLIDER_MM = -40.0
MAX_SLIDER_MM = 0.0


def _wrap(angle: float) -> float:
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def _rotate(point: tuple[float, float], angle: float) -> tuple[float, float]:
    c, s = math.cos(angle), math.sin(angle)
    return (c * point[0] - s * point[1], s * point[0] + c * point[1])


def solve_gripper(slider_m: float) -> tuple[float, float, float]:
    """Return rotor and positive/negative rod-joint angles for one slider command."""
    q_mm = min(MAX_SLIDER_MM, max(MIN_SLIDER_MM, slider_m * 1000.0))
    q = (SLIDER_PIN_POSITIVE[0], SLIDER_PIN_POSITIVE[1] + q_mm)
    distance = math.hypot(*q)
    along = (PIN_RADIUS**2 + distance**2 - LINK_LENGTH**2) / (2.0 * distance)
    height_sq = PIN_RADIUS**2 - along**2
    if height_sq < -1e-8:
        raise ValueError(f"No closed-linkage pose for slider command {slider_m} m")
    height = math.sqrt(max(0.0, height_sq))
    unit = (q[0] / distance, q[1] / distance)
    perpendicular = (-unit[1], unit[0])
    theta0 = math.atan2(ROTOR_PIN_POSITIVE[1], ROTOR_PIN_POSITIVE[0])
    candidates = []
    for sign in (-1.0, 1.0):
        pin = (
            along * unit[0] + sign * height * perpendicular[0],
            along * unit[1] + sign * height * perpendicular[1],
        )
        candidates.append(_wrap(math.atan2(pin[1], pin[0]) - theta0))
    rotor_angle = min(candidates, key=abs)

    rod_angles = []
    for sign, rotor_pin, slider_pin in (
        (1.0, ROTOR_PIN_POSITIVE, SLIDER_PIN_POSITIVE),
        (-1.0, ROTOR_PIN_NEGATIVE, SLIDER_PIN_NEGATIVE),
    ):
        moved_pin = _rotate(rotor_pin, rotor_angle)
        moved_slider = (slider_pin[0], slider_pin[1] + sign * q_mm)
        initial_rod_angle = math.atan2(
            slider_pin[1] - rotor_pin[1], slider_pin[0] - rotor_pin[0]
        )
        moved_rod_angle = math.atan2(
            moved_slider[1] - moved_pin[1], moved_slider[0] - moved_pin[0]
        )
        rod_angles.append(_wrap(moved_rod_angle - initial_rod_angle - rotor_angle))
    return rotor_angle, rod_angles[0], rod_angles[1]


def _self_check() -> None:
    for slider_mm in range(-40, 1):
        slider_m = slider_mm / 1000.0
        rotor, positive_rod, negative_rod = solve_gripper(slider_m)
        q_mm = slider_m * 1000.0
        for sign, rotor_pin, slider_pin, rod_angle in (
            (1.0, ROTOR_PIN_POSITIVE, SLIDER_PIN_POSITIVE, positive_rod),
            (-1.0, ROTOR_PIN_NEGATIVE, SLIDER_PIN_NEGATIVE, negative_rod),
        ):
            moved_pin = _rotate(rotor_pin, rotor)
            moved_slider = (slider_pin[0], slider_pin[1] + sign * q_mm)
            link_vector = (
                slider_pin[0] - rotor_pin[0],
                slider_pin[1] - rotor_pin[1],
            )
            rod_end = _rotate(link_vector, rotor + rod_angle)
            closed_end = (moved_pin[0] + rod_end[0], moved_pin[1] + rod_end[1])
            closure_error = math.hypot(
                closed_end[0] - moved_slider[0],
                closed_end[1] - moved_slider[1],
            )
            assert closure_error < 1e-6, f"Linkage pin centers separated by {closure_error} mm"

        assert abs(_wrap(positive_rod - negative_rod)) < 1e-6, "Mirrored rods diverged"
        for sign, rotor_pin, slider_pin in (
            (1.0, ROTOR_PIN_POSITIVE, SLIDER_PIN_POSITIVE),
            (-1.0, ROTOR_PIN_NEGATIVE, SLIDER_PIN_NEGATIVE),
        ):
            moved_pin = _rotate(rotor_pin, rotor)
            moved_slider = (slider_pin[0], slider_pin[1] + sign * q_mm)
            residual = abs(math.hypot(
                moved_slider[0] - moved_pin[0], moved_slider[1] - moved_pin[1]
            ) - LINK_LENGTH)
            assert residual < 1e-6, f"STEP rod length changed by {residual} mm"


def main() -> None:
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import JointState

    class GripperLinkageKinematics(Node):
        def __init__(self) -> None:
            super().__init__("gripper_linkage_kinematics")
            self.publisher = self.create_publisher(JointState, "joint_states", 10)
            self.subscription = self.create_subscription(
                JointState, "gui_joint_states", self.update, 10
            )

        def update(self, msg: JointState) -> None:
            positions = dict(zip(msg.name, msg.position))
            for side in ("left", "right"):
                prefix = f"openarm_{side}_gripper_"
                slider = positions.get(prefix + "close_joint", 0.0)
                rotor, positive_rod, negative_rod = solve_gripper(slider)
                positions[prefix + "rotor_joint"] = rotor
                positions[prefix + "link_positive_joint"] = positive_rod
                positions[prefix + "link_negative_joint"] = negative_rod
            output = JointState()
            output.header.stamp = self.get_clock().now().to_msg()
            output.name = list(positions)
            output.position = list(positions.values())
            self.publisher.publish(output)

    _self_check()
    rclpy.init()
    node = GripperLinkageKinematics()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

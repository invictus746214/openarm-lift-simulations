import unittest
import xml.etree.ElementTree as ET
import struct
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
XACRO = PACKAGE / "urdf" / "hei_lift_openarm_v20_aero_hands.urdf.xacro"
CONFIG = PACKAGE / "config" / "lift_arms_only.yaml"
LAUNCH = PACKAGE / "launch" / "display_lift_v20.launch.py"


class LiftV20Test(unittest.TestCase):
    def test_lift_moves_complete_robot_down_120_mm(self):
        root = ET.parse(XACRO).getroot()
        joint = root.find("./joint[@name='lift_joint']")
        self.assertIsNotNone(joint)
        self.assertEqual(joint.get("type"), "prismatic")
        self.assertEqual(joint.find("parent").get("link"), "lift_fixed_link")
        self.assertEqual(joint.find("child").get("link"), "lift_carriage_link")
        self.assertEqual(joint.find("axis").get("xyz"), "0 0 1")
        self.assertEqual(joint.find("limit").get("lower"), "-0.12")
        self.assertEqual(joint.find("limit").get("upper"), "0.0")

        config = CONFIG.read_text(encoding="utf-8")
        self.assertIn("root_frame: lift_carriage_link", config)
        self.assertIn("parent: lift_carriage_link", config)
        self.assertIn("origin: {x: 0.0, y: 0.0, z: 0.0", config)

    def test_lift_has_meshes_and_launch(self):
        fixed = PACKAGE / "meshes" / "hei_lift_fixed.STL"
        carriage = PACKAGE / "meshes" / "hei_lift_carriage.STL"
        self.assertTrue(fixed.is_file())
        self.assertTrue(carriage.is_file())
        with fixed.open("rb") as stream:
            stream.seek(80)
            triangles = struct.unpack("<I", stream.read(4))[0]
        self.assertLess(triangles, 600_000)
        self.assertTrue(LAUNCH.is_file())
        self.assertIn(
            "hei_lift_openarm_v20_aero_hands.urdf.xacro",
            LAUNCH.read_text(encoding="utf-8"),
        )
        source = LAUNCH.read_text(encoding="utf-8")
        self.assertIn("remove_link_visuals", source)
        self.assertIn('"openarm_body_link0"', source)
        self.assertNotIn('"openarm_left_joint1"', source)
        self.assertNotIn('"openarm_right_joint1"', source)

    def test_v20_connectors_and_flanges_match_cnc_aluminum(self):
        root = ET.parse(XACRO).getroot()
        for side in ("left", "right"):
            for part in ("connector", "flange"):
                material = root.find(
                    f"./link[@name='openarm_{side}_v20_{part}']/visual/material"
                )
                self.assertEqual(material.get("name"), "cnc_aluminum")


if __name__ == "__main__":
    unittest.main()

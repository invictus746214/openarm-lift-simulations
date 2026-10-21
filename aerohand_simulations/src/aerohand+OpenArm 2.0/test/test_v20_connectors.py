import struct
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
XACRO = PACKAGE / "urdf" / "openarm_v20_aero_hands.urdf.xacro"
LAUNCH = PACKAGE / "launch" / "display_v20.launch.py"
MESHES = PACKAGE / "meshes"


def binary_stl_triangle_count(path: Path) -> int:
    with path.open("rb") as stream:
        header = stream.read(84)
    if len(header) != 84:
        return 0
    return struct.unpack("<I", header[80:84])[0]


class V20ConnectorTest(unittest.TestCase):
    def test_measured_connector_chain_exists_for_both_hands(self):
        root = ET.parse(XACRO).getroot()

        for side in ("left", "right"):
            connector = root.find(f"./link[@name='openarm_{side}_v20_connector']")
            flange = root.find(f"./link[@name='openarm_{side}_v20_flange']")
            connector_joint = root.find(
                f"./joint[@name='openarm_{side}_v20_connector_mount']"
            )
            flange_joint = root.find(
                f"./joint[@name='openarm_{side}_v20_flange_mount']"
            )
            hand_joint = root.find(
                f"./joint[@name='openarm_{side}_v20_hand_mount']"
            )

            self.assertIsNotNone(connector)
            self.assertIsNotNone(flange)
            self.assertEqual(
                connector_joint.find("parent").get("link"),
                f"openarm_{side}_link7",
            )
            self.assertEqual(
                connector_joint.find("child").get("link"),
                f"openarm_{side}_v20_connector",
            )
            self.assertEqual(
                flange_joint.find("parent").get("link"),
                f"openarm_{side}_v20_connector",
            )
            self.assertEqual(
                flange_joint.find("child").get("link"),
                f"openarm_{side}_v20_flange",
            )
            self.assertEqual(
                hand_joint.find("parent").get("link"),
                f"openarm_{side}_v20_flange",
            )
            self.assertEqual(
                hand_joint.find("child").get("link"),
                f"{side}_base_link",
            )

    def test_all_four_measured_meshes_are_nonempty_binary_stl(self):
        for side in ("left", "right"):
            for part in ("connector", "flange"):
                mesh = MESHES / f"v20_{side}_{part}_on_link7.STL"
                self.assertTrue(mesh.is_file())
                self.assertGreater(binary_stl_triangle_count(mesh), 100)

    def test_connectors_and_flanges_match_cnc_aluminum(self):
        root = ET.parse(XACRO).getroot()
        for side in ("left", "right"):
            for part in ("connector", "flange"):
                material = root.find(
                    f"./link[@name='openarm_{side}_v20_{part}']/visual/material"
                )
                self.assertEqual(material.get("name"), "cnc_aluminum")

    def test_hand_mounts_are_local_to_the_step_j7_frame(self):
        root = ET.parse(XACRO).getroot()
        expected = {
            "left": [0.0, -0.0011, -0.0505],
            "right": [0.0, 0.0009, -0.0505],
        }
        for side in ("left", "right"):
            joint = root.find(
                f"./joint[@name='openarm_{side}_v20_hand_mount']"
            )
            xyz = [float(value) for value in joint.find("origin").get("xyz").split()]
            # STEP is globally offset -95 mm in its depth axis.  After that
            # assembly datum is removed, the hand base is 50.5 mm below link7.
            for actual, measured in zip(xyz, expected[side]):
                self.assertAlmostEqual(actual, measured, places=5)

    def test_v20_has_a_dedicated_launch_file(self):
        self.assertTrue(LAUNCH.is_file())
        source = LAUNCH.read_text(encoding="utf-8")
        self.assertIn("openarm_v20_aero_hands.urdf.xacro", source)


if __name__ == "__main__":
    unittest.main()

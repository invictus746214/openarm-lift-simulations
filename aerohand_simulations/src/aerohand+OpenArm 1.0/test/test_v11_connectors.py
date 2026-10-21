import struct
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
XACRO = PACKAGE / "urdf" / "openarm_v11_aero_hands.urdf.xacro"
MESHES = PACKAGE / "meshes"


def binary_stl_triangle_count(path: Path) -> int:
    with path.open("rb") as stream:
        header = stream.read(84)
    if len(header) != 84:
        return 0
    return struct.unpack("<I", header[80:84])[0]


class V11ConnectorTest(unittest.TestCase):
    def test_both_j8_a_connectors_are_attached_to_link7(self):
        root = ET.parse(XACRO).getroot()

        for side in ("left", "right"):
            link_name = f"openarm_{side}_j8_a_connector"
            joint_name = f"openarm_{side}_j8_a_mount"
            link = root.find(f"./link[@name='{link_name}']")
            joint = root.find(f"./joint[@name='{joint_name}']")

            self.assertIsNotNone(link)
            self.assertIsNotNone(joint)
            self.assertEqual(
                joint.find("parent").get("link"),
                f"openarm_{side}_link7",
            )
            self.assertEqual(joint.find("child").get("link"), link_name)

            mesh = link.find("./visual/geometry/mesh")
            self.assertEqual(
                mesh.get("filename"),
                f"package://aerohand_openarm_1_0/meshes/j8_a_{side}_on_link7.STL",
            )

    def test_connector_meshes_are_nonempty_binary_stl(self):
        for side in ("left", "right"):
            mesh = MESHES / f"j8_a_{side}_on_link7.STL"
            self.assertTrue(mesh.is_file())
            self.assertGreater(binary_stl_triangle_count(mesh), 100)

    def test_connectors_and_adapters_match_cnc_aluminum(self):
        root = ET.parse(XACRO).getroot()
        for side in ("left", "right"):
            for part in ("j8_a_connector", "aero_adapter"):
                material = root.find(
                    f"./link[@name='openarm_{side}_{part}']/visual/material"
                )
                self.assertEqual(material.get("name"), "cnc_aluminum")


if __name__ == "__main__":
    unittest.main()

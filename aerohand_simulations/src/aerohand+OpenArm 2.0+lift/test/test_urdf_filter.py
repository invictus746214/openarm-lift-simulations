import unittest

from aerohand_openarm_2_0_lift.urdf_filter import remove_link_visuals


SAMPLE_URDF = """\
<robot name="test">
  <link name="openarm_left_link7">
    <visual><geometry><box size="1 1 1"/></geometry></visual>
    <collision><geometry><box size="1 1 1"/></geometry></collision>
  </link>
  <link name="openarm_right_link7">
    <visual><geometry><box size="1 1 1"/></geometry></visual>
  </link>
  <link name="left_base_link">
    <visual><geometry><sphere radius="1"/></geometry></visual>
  </link>
  <joint name="left_mount" type="fixed">
    <parent link="openarm_left_link7"/>
    <child link="left_base_link"/>
  </joint>
</robot>
"""


class RemoveLinkVisualsTest(unittest.TestCase):
    def test_removes_only_requested_visuals_and_preserves_tree(self):
        filtered = remove_link_visuals(
            SAMPLE_URDF,
            {"openarm_left_link7", "openarm_right_link7"},
        )

        self.assertNotIn('<link name="openarm_left_link7"><visual>', filtered)
        self.assertNotIn('<link name="openarm_right_link7"><visual>', filtered)
        self.assertIn('<link name="openarm_left_link7">', filtered)
        self.assertIn("<collision>", filtered)
        self.assertIn('<link name="left_base_link">', filtered)
        self.assertIn("<visual>", filtered)
        self.assertIn('<joint name="left_mount" type="fixed">', filtered)

    def test_rejects_unknown_target_link(self):
        with self.assertRaisesRegex(ValueError, "missing_link"):
            remove_link_visuals(SAMPLE_URDF, {"missing_link"})


if __name__ == "__main__":
    unittest.main()

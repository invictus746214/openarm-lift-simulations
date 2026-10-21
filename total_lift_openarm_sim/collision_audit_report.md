# Collision screening

> Historical reference only: the AABB counts below predate the official OpenArm wrist link4-link6 replacement. They do not describe the current URDF's collision geometry or prove surface clearance.

## Method and scope

- Transformed the URDF collision meshes and screened 154 poses using world-frame axis-aligned bounding boxes.
- For each arm, sampled J2 and J6 at 9 evenly spaced values, combined with all four lift travel corners (0/0.319 m and 0/0.288 m). Also sampled each gripper at 0, -10, -20, -30, and -40 mm.
- Screening considered 42 arm-to-lift link pairs and 8 rod-to-jaw pairs. Direct parent-child pairs were excluded.
- An AABB overlap means the meshes may be near or intersecting. It does not prove that their triangle surfaces intersect; broad boxes can overlap while the actual parts remain separated.

## Potential arm-to-lift overlaps

| Link pair | Sampled poses with overlapping bounds |
|---|---:|
| `lift_upper_link | openarm_left_link0` | 72 |
| `lift_upper_link | openarm_left_link3` | 4 |
| `lift_base_link | openarm_left_link3` | 12 |
| `lift_base_link | openarm_left_link4` | 11 |
| `lift_base_link | openarm_left_link5` | 30 |
| `lift_base_link | openarm_left_link6` | 30 |
| `lift_middle_link | openarm_left_link5` | 4 |
| `lift_middle_link | openarm_left_link6` | 4 |
| `lift_upper_link | openarm_left_link4` | 4 |
| `lift_upper_link | openarm_left_link5` | 4 |
| `lift_upper_link | openarm_left_link6` | 12 |
| `lift_base_link | openarm_right_link3` | 22 |
| `lift_base_link | openarm_right_link4` | 21 |
| `lift_base_link | openarm_right_link5` | 40 |
| `lift_base_link | openarm_right_link6` | 40 |
| `lift_middle_link | openarm_right_link6` | 4 |
| `lift_upper_link | openarm_right_link0` | 82 |
| `lift_upper_link | openarm_right_link3` | 4 |
| `lift_upper_link | openarm_right_link4` | 4 |
| `lift_upper_link | openarm_right_link5` | 4 |
| `lift_upper_link | openarm_right_link6` | 12 |

## Gripper rod-to-jaw screening

No rod-to-jaw AABB overlaps appeared in the five sampled closure positions per gripper. This does not rule out thin-surface contact.

## Limits

- 21 arm-to-lift link pairs have potential bounding-box overlaps in the sampled states. Some may be intended mounting interfaces; exact triangle intersection and penetration depth were not established for this update.
- VTK triangle-level sweep was stopped because repeated surface checks were too slow in this Windows environment. A MoveIt collision checker or a faster mesh-BVH sweep is needed to confirm these candidates and check unsampled combined poses.
- The RViz package displays collision meshes but does not prevent penetration while sliders move.

## Restored J4-J5 covers (2026-10-15)

- VTK triangle-mesh collision checks compared each restored cover on link4 with adjacent link3 and link5 collision meshes at 9 sampled J4/J5 combinations per arm: J4 = 0/1.22/2.44 rad and J5 = -1.2/0/1.2 rad.
- No triangle intersections were found for those cover-to-link3/link5 pairs in the 18 sampled poses.
- This is a local pose sample; it does not verify cover clearance against the lift, the rest of the robot, or every possible joint pose.

## Restored J5-J6 side connectors (2026-10-15)

- The two long STEP parts `J6_A` and `J6_B` on each arm are attached to link5, between J5 and J6, using their STEP placements relative to the official OpenArm link5 frame.
- VTK triangle-mesh checks compared both connectors on each arm with link4, the J4-J5 cover, and link6 at 9 J5/J6 combinations per arm: J5 = -1.2/0/1.2 rad and J6 = -0.6/0/0.6 rad.
- No triangle intersections were found in those 18 sampled poses. This local sample does not establish full-robot clearance, penetration depth, or clearance at every joint pose.

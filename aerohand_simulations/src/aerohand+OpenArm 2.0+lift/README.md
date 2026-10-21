# aerohand + OpenArm 2.0 + lift

OpenArm v2.0、Aero Hand 左右手与升降滑台组合的 RViz 运动学可视化；滑台行程为 120 mm。

在 ROS 2 Humble 工作区构建后运行：

ros2 launch aerohand_openarm_2_0_lift display_lift_v20.launch.py

该包依赖工作区中的 aerohand 和 openarm_description；连接件网格在本包的 meshes/，模型入口在 urdf/。许可与 STEP 衍生网格说明见本目录 LICENSES/ 和仓库根目录说明。
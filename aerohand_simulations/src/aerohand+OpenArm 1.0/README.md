# aerohand + OpenArm 1.0

OpenArm v1.0 双臂、Aero Hand 左右手及 J8 转接件的 RViz 运动学可视化。

在 ROS 2 Humble 工作区构建后运行：

ros2 launch aerohand_openarm_1_0 display_v11.launch.py

该包依赖工作区中的 aerohand 和 openarm_description；连接件网格在本包的 meshes/，模型入口在 urdf/。许可与 STEP 衍生网格说明见本目录 LICENSES/ 和仓库根目录说明。
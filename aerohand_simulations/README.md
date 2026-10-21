# AeroHand 与 OpenArm RViz 仿真包

这里整理了四套可分别启动的 ROS 2 描述包。每个版本目录本身就是 ROS 包根目录，打开后能直接看到 launch、meshes、rviz、urdf、package.xml 等文件。OpenArm 官方描述作为工作区公共依赖只保留一份。

## 四个版本

| 目录 | ROS 包名 | 用途 | 启动命令 |
|---|---|---|---|
| src/aerohand | aerohand | 官方 AeroHand 左右手模型 | ros2 launch aerohand display.launch.py |
| src/aerohand+OpenArm 1.0 | aerohand_openarm_1_0 | AeroHand + OpenArm 1.0 | ros2 launch aerohand_openarm_1_0 display_v11.launch.py |
| src/aerohand+OpenArm 2.0 | aerohand_openarm_2_0 | AeroHand + OpenArm 2.0 | ros2 launch aerohand_openarm_2_0 display_v20.launch.py |
| src/aerohand+OpenArm 2.0+lift | aerohand_openarm_2_0_lift | AeroHand + OpenArm 2.0 + 120 mm 升降滑台 | ros2 launch aerohand_openarm_2_0_lift display_lift_v20.launch.py |

目录名是便于辨认的版本名称；ROS 包名使用小写下划线，记录在各自 package.xml 中。三个组合包依赖同一工作区里的 aerohand 和 openarm_description。

## Ubuntu 22.04 / ROS 2 Humble

在此文件夹根目录打开终端，安装依赖并构建：

```bash
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

然后复制上表中需要的启动命令。切换版本前在当前终端按 Ctrl+C 关闭上一套 RViz。

## 目录结构

```text
src/
  aerohand/
    launch/ LICENSES/ meshes/ resource/ rviz/ urdf/
    package.xml setup.py setup.cfg
  aerohand+OpenArm 1.0/
    launch/ LICENSES/ meshes/ rviz/ urdf/ test/
    aerohand_openarm_1_0/       # launch 使用的 URDF 过滤器
    CMakeLists.txt package.xml
  aerohand+OpenArm 2.0/
    config/ launch/ LICENSES/ meshes/ rviz/ urdf/ test/
    CMakeLists.txt package.xml
  aerohand+OpenArm 2.0+lift/
    config/ launch/ LICENSES/ meshes/ rviz/ urdf/ test/
    aerohand_openarm_2_0_lift/  # launch 使用的 URDF 过滤器
    CMakeLists.txt package.xml
  openarm_description/          # OpenArm 官方共享描述与网格
```

这些启动文件用于关节滑块和 RViz 运动学可视化，不含动力学/碰撞仿真或实体机器人驱动。组合包保留了原有的连接件、滑台和 URDF 过滤检查。

## 许可

各部分许可不同，请先阅读 THIRD_PARTY_NOTICES.md 和 AERO_HAND_OPEN_LICENSE.md。连接件和升降滑台网格来自你提供的 STEP；公开上传前请确认 STEP 衍生文件可以再分发。此目录目前只在本地，未上传 GitHub。
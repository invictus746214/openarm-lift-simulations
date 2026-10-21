# OpenArm 与 AeroHand ROS 2 RViz 模型合集

本仓库收录两套独立的 ROS 2 模型工程：Aero Hand 与 OpenArm 的组合模型，以及双级升降柱 OpenArm 总装模型。模型使用 URDF/Xacro 和 STL 网格，在 RViz 2 中查看装配关系并通过关节滑块观察运动。

## 项目内容

| 路径 | 内容 | 详细说明 |
| --- | --- | --- |
| [`aerohand_simulations/`](aerohand_simulations/) | Aero Hand 左右手、OpenArm v1.0/v2.0 组合，以及 v2.0 升降架配置 | [AeroHand 项目说明](aerohand_simulations/README.md) |
| [`total_lift_openarm_sim/`](total_lift_openarm_sim/) | 双级升降柱、OpenArm v1.1 总装、左右夹爪闭环运动显示 | [总装项目说明](total_lift_openarm_sim/README.md) |

两个项目分别构建，不需要合并为一个 ROS 包。AeroHand 项目在 `src/` 中共享 Aero Hand 和 OpenArm 描述资源；组合配置只保留各自的 URDF、launch、RViz 配置和必要的集成代码。

## 运行环境

- Ubuntu 22.04
- ROS 2 Humble
- `colcon`、RViz 2、Xacro、Robot State Publisher、Joint State Publisher GUI

安装常用工具：

```bash
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  ros-humble-xacro \
  ros-humble-rviz2 \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher-gui
```

## Aero Hand 与 OpenArm 配置

在仓库目录下运行：

```bash
cd <仓库路径>/aerohand_simulations
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

然后选择一种配置启动：

| 模型 | 命令 |
| --- | --- |
| Aero Hand 左右手 | `ros2 launch aerohand display.launch.py` |
| OpenArm v1.0 + Aero Hand | `ros2 launch aerohand_openarm_1_0 display_v11.launch.py` |
| OpenArm v2.0 + Aero Hand | `ros2 launch aerohand_openarm_2_0 display_v20.launch.py` |
| OpenArm v2.0 + Aero Hand + 升降架 | `ros2 launch aerohand_openarm_2_0_lift display_lift_v20.launch.py` |

每个启动文件会打开对应的 RViz 模型视图和关节滑块。切换配置前，先在当前终端按 `Ctrl+C` 关闭正在运行的实例。

## 双级升降柱总装模型

`total_lift_openarm_sim/` 是独立 ROS 2 包。首次构建时，从仓库根目录把它链接到工作区 `src/`，然后编译并启动：

```bash
cd <仓库路径>
mkdir -p ~/ros2_ws/src
ln -s "$PWD/total_lift_openarm_sim" ~/ros2_ws/src/total_lift_openarm_sim

# 若当前终端启用了 Conda，先退出，避免 CMake 选错 Python。
if [ -n "${CONDA_PREFIX:-}" ] && command -v conda >/dev/null 2>&1; then conda deactivate; fi

source /opt/ros/humble/setup.bash
cd ~/ros2_ws
colcon build --packages-select total_lift_openarm_sim \
  --cmake-clean-cache \
  --cmake-args -DPython3_EXECUTABLE=/usr/bin/python3
source install/setup.bash
ros2 launch total_lift_openarm_sim display.launch.py
```

启动后，Joint State Publisher GUI 控制两段沿 Z 轴伸缩的升降柱、左右 OpenArm 关节和夹爪。夹爪转子与连杆由包内闭环解算节点更新。关节行程和速度/力矩占位值只用于模型显示，不代表实机参数。

## 仿真范围

这些工程用于 RViz 中的模型展示和运动学观察，不含实体机器人驱动，也不提供完整动力学仿真。RViz 的关节滑块不会自动阻止网格互相穿透；总装项目的局部碰撞检查结果和限制见其 `collision_audit_report.md` 及项目说明。需要 Gazebo 或 MoveIt 仿真时，应另行配置对应的物理参数、控制器和碰撞规则。

## 许可与来源

不同文件适用不同许可，请先阅读各项目附带的许可文件和 [`THIRD_PARTY_NOTICES.md`](aerohand_simulations/THIRD_PARTY_NOTICES.md)：

- Aero Hand 硬件设计文件与文档按 **CC BY-NC-SA 4.0** 提供；代码许可另见随附的 Apache-2.0 文本。分享硬件文件或其修改版本时需保留署名、遵守非商业和相同方式共享要求。
- OpenArm 官方描述与网格按其随附的 **Apache-2.0** 文件提供。
- OpenArm 集成代码与升降柱、连接件等 STEP 派生网格的许可可能不同。代码许可证不会自动授予 STEP 派生网格的再分发权；公开分享这些网格前，需确认自己拥有相应授权。

原始 STEP 装配文件不包含在本仓库中。使用者应按各文件随附的许可和来源说明使用、修改或再分发内容。

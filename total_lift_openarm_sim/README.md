# 总装升降柱 + OpenArm v1.1（ROS 2 Humble）

底盘、升降柱、OpenArm 胸部及近端连杆、夹爪网格由 STEP 总装导出。左右手腕 link4–link6 使用官方 OpenArm v1.0 网格和 J5/J6/J7 关节定义。STEP 中两件 `J4-J5_Cover_v1.0` 分别挂在左右 link4，随 J4 运动；每只手的 `J6_A`、`J6_B` 两片长条连接板按 STEP 相对位置挂在 link5，连接 J5 与 J6，并随 J5 一起运动。STEP 的左右 `J7_D` 连接件单独导出到 link7 的 J7 后坐标系，随 J7 一起运动；夹爪仍用原有 STEP 几何和闭环开合机构，安装补偿不变。升降柱三段使用统一颜色。

## 可动部分

- `lift_stage1_joint`：中方管沿 +Z 伸出，行程 0.319 m。SolidWorks 距离限位为 6–325 mm，URDF 把 STEP 当前姿态定为零点。
- `lift_stage2_joint`：小方管与顶部安装组件沿 +Z 伸出，行程 0.288 m。SolidWorks 距离限位为 7–295 mm，同样以 STEP 当前姿态为零点。
- 左右 OpenArm 各有 7 个旋转关节，可在 Joint State Publisher 窗口拖动。
- J5/J6/J7 使用官方 OpenArm v1.0 的关节原点、方向及左右手镜像，link4–link6 使用其腕部网格。先前把 J6 原点移低 74 mm、再用 J7 补偿 75 mm 的做法已撤销；那会让零位接近，却在运动时使腕部断开。旧版补的显示销轴已移除。官方 link7 网格与现有夹爪电机重叠，因此只恢复 STEP 中独立的 `J7_D` 连接件，不加载整块官方 link7 网格；它固定在 J7 输出侧，随 J5/J6/J7 的运动链运动，原夹爪外观、安装和开合保持不变。
- 每侧夹爪的 STEP 几何拆成驱动转子、两根 `swivel_link` 连杆和两套 jaw/滑块。按夹爪局部坐标核对，转子销中心是 `(-27.823872, 28.737296)` / `(27.823872, -28.737296) mm`，滑块销中心是 `(-18.600, 62.500)` / `(18.600, -62.500) mm`；所有转轴平行于 Z。曲柄半径为 40 mm、连杆中心距为 35 mm；STEP 中连杆孔与转子销轴线的偏差为 0.00033 mm，连杆与滑块端轴承轴线偏差小于 0.001 mm。两根连杆以转子中心为轴在 XY 平面旋转 180° 后完全重合；两套 jaw/滑块参考点位于 `Y=±62.5 mm`，jaw 外包络关于 `Y=0` 镜像，误差小于 0.001 mm，不会出现一侧在中心、另一侧跑到边上的错位。
- `openarm_left_gripper_close_joint` 和 `openarm_right_gripper_close_joint` 分别控制左右夹爪，另一滑块由 URDF mimic 反向同步。显示启动文件附带闭环解算节点，按测得的曲柄滑块几何计算转子和连杆角度，使杆端随滑块保持同心。滑块从 0 到 -0.04 m 表示由张开到闭合。
- STEP 中每个滑块的 8 颗 `kbbs3-6` 和 2 颗 `cbe3-5` 螺丝并入对应滑块网格；每侧转子上的 4 颗 `cbe3-8` 螺丝及偏心轴承/衬套随转子运动，固定在电机壳体上的另外 6 颗 `cbe3-8` 留在固定网格中。
- 按截图去掉每侧夹爪滑块外端各两个外露圆环：对应 `MR126ZZ` 轴承和 `DBSY4-5-4` 衬套在局部 `Y=±62.5 mm` 的端点位置；转子侧连杆支点保留。
- GUI 每侧只显示一个夹爪开合滑块；转子和两根连杆关节由闭环解算节点驱动，不作为独立滑块。
- 启动脚本用过滤后的临时 URDF 初始化滑块 GUI，并隔离完整模型描述话题，避免滑块被全量关节列表覆盖。
- 中方管、小方管可在 Joint State Publisher 中分别拖动；关节滑块限位是按当前 STEP 姿态设定的仿真显示范围。

RViz 中 Fixed Frame 是 `world`，RobotModel 会由启动文件自动加载；默认配置不显示 TF 坐标轴，避免坐标标记看起来像模型细线。STEP 和官方手腕网格单位均为 mm，URDF 用 0.001 缩放。

URDF 为外观网格配了碰撞几何；官方腕部使用其简化碰撞网格。`collision_audit_report.md` 中的局部三角网格检查覆盖 J4-J5 罩壳，以及 J5-J6 长条连接板与 link4、link6，在各自 9 组采样姿态下未发现相交。旧全身 J2/J6 包围盒筛查仍基于替换前网格，不能代表当前全身碰撞结果。RViz 关节滑块不会执行碰撞判定或阻止零件穿透；MoveIt 等碰撞检查器需要另配碰撞允许矩阵。

## Ubuntu / ROS 2 Humble

将仓库目录放到 `~/ros2_ws/src/total_lift_openarm_sim`。需要 ROS 2 Humble（含 RViz）和 `colcon`。在同一个新终端执行：

```bash
# 如果当前使用 Conda，先退出，避免 CMake 选错 Python
if [ -n "${CONDA_PREFIX:-}" ] && command -v conda >/dev/null 2>&1; then conda deactivate; fi
source /opt/ros/humble/setup.bash
cd ~/ros2_ws
colcon build --packages-select total_lift_openarm_sim --cmake-clean-cache --cmake-args -DPython3_EXECUTABLE=/usr/bin/python3
source install/setup.bash
ros2 launch total_lift_openarm_sim display.launch.py
```

启动后会打开关节滑块 GUI、夹爪闭环解算节点和 RViz。拖动左右夹爪各自的 `gripper_close_joint` 滑块即可开合；转子与两根连杆由解算节点更新。

STEP 文件不保存 SolidWorks 配合定义；腕部采用官方 v1.0 定义来近似 v1.1 STEP 装配。此模型面向 RViz 关节运动显示，不含实测惯性或 Gazebo 物理插件。升降和夹爪关节的 effort/velocity 是 GUI 占位值，不是执行器参数。官方网格及来源许可见 `LICENSES`。

发布前请确认 `meshes/step_*.stl` 和 `meshes/openarm_*.stl` 等 STEP 派生模型具有公开再分发授权；OpenArm 的 Apache-2.0 许可不自动覆盖这些网格。原始 STEP 文件未放入本仓库。

cmake_minimum_required(VERSION 3.8)
project(aerohand_openarm_2_0_lift)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
ament_python_install_package(aerohand_openarm_2_0_lift)

install(DIRECTORY LICENSES config launch meshes rviz urdf
  DESTINATION share/aerohand_openarm_2_0_lift)

ament_package()
if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_lift_v20 test/test_lift_v20.py)
  ament_add_pytest_test(test_urdf_filter test/test_urdf_filter.py)
endif()

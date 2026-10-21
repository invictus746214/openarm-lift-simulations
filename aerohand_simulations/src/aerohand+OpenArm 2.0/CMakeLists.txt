cmake_minimum_required(VERSION 3.8)
project(aerohand_openarm_2_0)

find_package(ament_cmake REQUIRED)

install(DIRECTORY LICENSES config launch meshes rviz urdf
  DESTINATION share/aerohand_openarm_2_0)

ament_package()
if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_v20_connectors test/test_v20_connectors.py)
endif()

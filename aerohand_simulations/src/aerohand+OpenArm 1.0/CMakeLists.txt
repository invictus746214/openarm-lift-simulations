cmake_minimum_required(VERSION 3.8)
project(aerohand_openarm_1_0)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
ament_python_install_package(aerohand_openarm_1_0)

install(DIRECTORY LICENSES launch meshes rviz urdf
  DESTINATION share/aerohand_openarm_1_0)

ament_package()
if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_v11_connectors test/test_v11_connectors.py)
  ament_add_pytest_test(test_urdf_filter test/test_urdf_filter.py)
endif()

cmake_minimum_required(VERSION 3.0.2)
project(ros-flask)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

catkin_package(
   INCLUDE_DIRS web
#  LIBRARIES ros-flask
#  CATKIN_DEPENDS roscpp rospy std_msgs Flask
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
   src/http_server.py
   src/video_processor.py
   src/webcam.py
   web/index.html
   src/__init__.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
 )

install(FILES
    web/index.html
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
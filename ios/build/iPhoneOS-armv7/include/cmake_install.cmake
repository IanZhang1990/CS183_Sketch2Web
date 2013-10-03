# Install script for directory: /Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/ios/build/iPhoneOS-armv7/install")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "main")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv" TYPE FILE FILES
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cv.h"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cv.hpp"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cvaux.h"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cvaux.hpp"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cvwimage.h"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cxcore.h"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cxcore.hpp"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cxeigen.hpp"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/cxmisc.h"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/highgui.h"
    "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv/ml.h"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "main")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "main")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2" TYPE FILE FILES "/Users/IanZhang/Documents/CS183/CS183_Sketch2Web/opencv-2.4.6.1/include/opencv2/opencv.hpp")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "main")


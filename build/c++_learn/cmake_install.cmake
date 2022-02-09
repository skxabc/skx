# Install script for directory: /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/classSize/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/lambda/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/file/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/helloWorld/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/webocketClient/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/mergeFile/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/regex/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/cjson/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/BFS/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/DFS/cmake_install.cmake")
  include("/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/udp/cmake_install.cmake")

endif()


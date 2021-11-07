PROJECT(SPEEX)
cmake_minimum_required(VERSION 3.13)
ADD_SUBDIRECTORY(src bin)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib/speex/include)

link_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib/speex/lib)
message(STATUS "CMakeLists.txt src enter")
ADD_EXECUTABLE(hello main.c)
ADD_LIBRARY(skxhello SHARED main.c)
#SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)
#SET(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)

INSTALL(TARGETS hello skxhello
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
)
message(STATUS "CMakeLists.txt src leave")

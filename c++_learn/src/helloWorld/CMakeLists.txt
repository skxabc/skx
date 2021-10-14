project(skx)
add_executable(hello hello.cpp)

target_link_libraries(hello pthread)
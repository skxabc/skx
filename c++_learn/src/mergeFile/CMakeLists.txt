project(skx)
add_executable(mergefile merge_opus_files_2_1.cpp)

target_link_libraries(mergefile pthread)

add_executable(speex mytest.c myspeex.c)

include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${PROJECT_SOURCE_DIR}/lib/speex/include)

target_link_libraries(speex ${PROJECT_SOURCE_DIR}/lib/speex/lib/libspeex.so)
target_link_libraries(speex m)
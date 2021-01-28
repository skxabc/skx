SET(LIBHELLO_SRC hello.c)
ADD_LIBRARY(hello SHARED ${LIBHELLO_SRC})
ADD_LIBRARY(hello_static ${LIBHELLO_SRC})

#set the library output path
SET(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/skxshare)

#rename the static library and add version to the shared library
SET_TARGET_PROPERTIES(hello_static PROPERTIES OUTPUT_NAME "hello")
SET_TARGET_PROPERTIES(hello PROPERTIES VERSION 1.2 SOVERSION 1)

INSTALL(TARGETS hello hello_static
        LIBRARY DESTINATION lib/hello 
        ARCHIVE DESTINATION lib/hello
)
INSTALL(FILES hello.h DESTINATION include/hello)

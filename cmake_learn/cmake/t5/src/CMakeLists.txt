
ADD_EXECUTABLE(curltest main.c)
FIND_PACKAGE(CURL)
IF(CURL_FOUND)
INCLUDE_DIRECTORIES(${CURL_INCLUDE_DIR})
MESSAGE(STATUS "curl include:" ${CURL_INCLUDE_DIR})
TARGET_LINK_LIBRARIES(curltest ${CURL_LIBRARY})
MESSAGE(STATUS "curl library:" ${CURL_LIBRARY})
ENDIF(CURL_FOUND)
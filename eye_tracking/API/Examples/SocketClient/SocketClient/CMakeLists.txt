cmake_minimum_required(VERSION 3.10)
project(SocketClient LANGUAGES CXX)

if(NOT DEFINED SocketClient_SEP_API_INCLUDE_DIR)
  set(SocketClient_SEP_API_INCLUDE_DIR "C:/Program Files/Smart Eye/Smart Eye Pro X.Y/API/include")
endif()
message(STATUS "SocketClient_SEP_API_INCLUDE_DIR: ${SocketClient_SEP_API_INCLUDE_DIR}")

set(SRCS
  src/SocketClient.cpp
)

add_executable(SocketClient ${SRCS})
set_target_properties(
    SocketClient
  PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED True
)
target_compile_options(SocketClient PRIVATE /W4 /WX)
target_include_directories(SocketClient PRIVATE ${SocketClient_SEP_API_INCLUDE_DIR})

cmake_minimum_required(VERSION 3.10)

project(RPCExample)

# SeJsonRpc related paths. By default these are all found in the Smart Eye Pro
# API/Examples/bin directory.
if(NOT DEFINED RPCExample_SEP_BIN_DIR)
  set(RPCExample_SEP_BIN_DIR "C:/Program Files/Smart Eye/Smart Eye Pro X.Y/API/Examples/bin")
endif()
if(NOT DEFINED RPCExample_SEP_API_INCLUDE_DIR)
  set(RPCExample_SEP_API_INCLUDE_DIR "C:/Program Files/Smart Eye/Smart Eye Pro X.Y/API/include")
endif()

if(NOT DEFINED RPCExample_SEJSONRPC_INCLUDE_DIR)
  set(RPCExample_SEJSONRPC_INCLUDE_DIR "${RPCExample_SEP_BIN_DIR}")
endif()
if(NOT DEFINED RPCExample_SEJSONRPC_LIB)
  set(RPCExample_SEJSONRPC_LIB "${RPCExample_SEP_BIN_DIR}/SeJsonRpc.lib")
endif()
if(NOT DEFINED RPCExample_SEJSONRPC_DLL)
  set(RPCExample_SEJSONRPC_DLL "${RPCExample_SEP_BIN_DIR}/SeJsonRpc.dll")
endif()
if(NOT DEFINED RPCExample_COPY_DLL)
  set(RPCExample_COPY_DLL ON)
endif()

message(STATUS "RPCExample_SEJSONRPC_INCLUDE_DIR: ${RPCExample_SEJSONRPC_INCLUDE_DIR}")
message(STATUS "RPCExample_SEJSONRPC_LIB: ${RPCExample_SEJSONRPC_LIB}")
message(STATUS "RPCExample_SEJSONRPC_DLL: ${RPCExample_SEJSONRPC_DLL}")
message(STATUS "RPCExample_COPY_DLL: ${RPCExample_COPY_DLL}")
message(STATUS "RPCExample_SEP_API_INCLUDE_DIR: ${RPCExample_SEP_API_INCLUDE_DIR}")

set(SRCS
    src/main.cpp
    src/Simple.cpp
    src/TrackAndRec.cpp
    src/GetSetProfile.cpp
)
set(INCLUDES
    inc/RpcHandle.h
    inc/Simple.h
    inc/TrackAndRec.h
    inc/GetSetProfile.h
)
set(INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/inc")

add_executable(RPCExample ${SRCS} ${INCLUDES})
set_target_properties(
  RPCExample
  PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED True
)
target_compile_options(RPCExample PRIVATE /W4 /WX)
target_include_directories(RPCExample PRIVATE ${RPCExample_SEJSONRPC_INCLUDE_DIR} ${INCLUDE_DIR} ${RPCExample_SEP_API_INCLUDE_DIR})
target_link_libraries(RPCExample ${RPCExample_SEJSONRPC_LIB})

# Copy SEJsonRpc.dll to output.
if(RPCExample_COPY_DLL)
  add_custom_command(
    TARGET RPCExample
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${RPCExample_SEJSONRPC_DLL}
            ${CMAKE_CURRENT_BINARY_DIR}/$<CONFIG>/SEJsonRpc.dll
  )
endif()

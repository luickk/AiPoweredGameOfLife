cmake_minimum_required (VERSION 3.8)

project(TestGame)

add_executable(TestGame game.c)

#find_library(TENSORFLOW_LIBRARIES tensorflow)
#find_path(TENSORFLOW_INCLUDE_DIRS tensorflow)
#if(NOT TENSORFLOW_LIBRARIES OR NOT TENSORFLOW_INCLUDE_DIRS)
#  message(FATAL_ERROR "TENSORFLOW lib or include not found")
#endif()
#include_directories(${TENSORFLOW_INCLUDE_DIRS})
#target_link_libraries (TestGame ${TENSORFLOW_LIBRARIES})

target_link_libraries(TestGame ${CMAKE_BINARY_DIR}/src/libGameOfLife.a)

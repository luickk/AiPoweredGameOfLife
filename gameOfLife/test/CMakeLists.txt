cmake_minimum_required (VERSION 3.8)

project(TestGame)

add_executable(TestGame game.c)

target_link_libraries(TestGame ${CMAKE_BINARY_DIR}/src/libGameOfLife.a)

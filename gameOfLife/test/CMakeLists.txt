cmake_minimum_required (VERSION 3.8)

project(TestGame)

find_library(TENSORFLOW_LIBRARIES tensorflow)

find_path(TENSORFLOW_INCLUDE_DIRS tensorflow)

if(NOT TENSORFLOW_LIBRARIES OR NOT TENSORFLOW_INCLUDE_DIRS)
  message(FATAL_ERROR "TENSORFLOW lib or include not found")
endif()

add_executable(TestGame game.c)


include_directories(${TENSORFLOW_INCLUDE_DIRS})


target_link_libraries (TestGame ${TENSORFLOW_LIBRARIES})

# include_directories(/usr/local/include)
# link_directories(TestGame /usr/local/bin)

target_link_libraries(TestGame ${CMAKE_BINARY_DIR}/src/libGameOfLife.a)

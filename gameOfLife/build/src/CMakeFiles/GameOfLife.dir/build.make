# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.18.4/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.18.4/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build

# Include any dependencies generated for this target.
include src/CMakeFiles/GameOfLife.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/GameOfLife.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/GameOfLife.dir/flags.make

src/CMakeFiles/GameOfLife.dir/gameOfLife.c.o: src/CMakeFiles/GameOfLife.dir/flags.make
src/CMakeFiles/GameOfLife.dir/gameOfLife.c.o: ../src/gameOfLife.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object src/CMakeFiles/GameOfLife.dir/gameOfLife.c.o"
	cd /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/src && /Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/GameOfLife.dir/gameOfLife.c.o -c /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/src/gameOfLife.c

src/CMakeFiles/GameOfLife.dir/gameOfLife.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/GameOfLife.dir/gameOfLife.c.i"
	cd /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/src && /Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/src/gameOfLife.c > CMakeFiles/GameOfLife.dir/gameOfLife.c.i

src/CMakeFiles/GameOfLife.dir/gameOfLife.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/GameOfLife.dir/gameOfLife.c.s"
	cd /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/src && /Library/Developer/CommandLineTools/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/src/gameOfLife.c -o CMakeFiles/GameOfLife.dir/gameOfLife.c.s

# Object files for target GameOfLife
GameOfLife_OBJECTS = \
"CMakeFiles/GameOfLife.dir/gameOfLife.c.o"

# External object files for target GameOfLife
GameOfLife_EXTERNAL_OBJECTS =

src/libGameOfLife.a: src/CMakeFiles/GameOfLife.dir/gameOfLife.c.o
src/libGameOfLife.a: src/CMakeFiles/GameOfLife.dir/build.make
src/libGameOfLife.a: src/CMakeFiles/GameOfLife.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C static library libGameOfLife.a"
	cd /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/src && $(CMAKE_COMMAND) -P CMakeFiles/GameOfLife.dir/cmake_clean_target.cmake
	cd /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/GameOfLife.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/GameOfLife.dir/build: src/libGameOfLife.a

.PHONY : src/CMakeFiles/GameOfLife.dir/build

src/CMakeFiles/GameOfLife.dir/clean:
	cd /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/src && $(CMAKE_COMMAND) -P CMakeFiles/GameOfLife.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/GameOfLife.dir/clean

src/CMakeFiles/GameOfLife.dir/depend:
	cd /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/src /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/src /Users/luickklippel/Documents/Projekte/AiPoweredGameOfLife/gameOfLife/build/src/CMakeFiles/GameOfLife.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/GameOfLife.dir/depend


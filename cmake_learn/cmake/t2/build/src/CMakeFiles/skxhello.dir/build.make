# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/shikaixun/test/skx/cmake_learn/cmake/t2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/shikaixun/test/skx/cmake_learn/cmake/t2/build

# Include any dependencies generated for this target.
include src/CMakeFiles/skxhello.dir/depend.make

# Include the progress variables for this target.
include src/CMakeFiles/skxhello.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/skxhello.dir/flags.make

src/CMakeFiles/skxhello.dir/main.c.o: src/CMakeFiles/skxhello.dir/flags.make
src/CMakeFiles/skxhello.dir/main.c.o: ../src/main.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/shikaixun/test/skx/cmake_learn/cmake/t2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object src/CMakeFiles/skxhello.dir/main.c.o"
	cd /home/shikaixun/test/skx/cmake_learn/cmake/t2/build/src && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/skxhello.dir/main.c.o   -c /home/shikaixun/test/skx/cmake_learn/cmake/t2/src/main.c

src/CMakeFiles/skxhello.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/skxhello.dir/main.c.i"
	cd /home/shikaixun/test/skx/cmake_learn/cmake/t2/build/src && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/shikaixun/test/skx/cmake_learn/cmake/t2/src/main.c > CMakeFiles/skxhello.dir/main.c.i

src/CMakeFiles/skxhello.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/skxhello.dir/main.c.s"
	cd /home/shikaixun/test/skx/cmake_learn/cmake/t2/build/src && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/shikaixun/test/skx/cmake_learn/cmake/t2/src/main.c -o CMakeFiles/skxhello.dir/main.c.s

# Object files for target skxhello
skxhello_OBJECTS = \
"CMakeFiles/skxhello.dir/main.c.o"

# External object files for target skxhello
skxhello_EXTERNAL_OBJECTS =

src/libskxhello.so: src/CMakeFiles/skxhello.dir/main.c.o
src/libskxhello.so: src/CMakeFiles/skxhello.dir/build.make
src/libskxhello.so: src/CMakeFiles/skxhello.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/shikaixun/test/skx/cmake_learn/cmake/t2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C shared library libskxhello.so"
	cd /home/shikaixun/test/skx/cmake_learn/cmake/t2/build/src && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/skxhello.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/CMakeFiles/skxhello.dir/build: src/libskxhello.so

.PHONY : src/CMakeFiles/skxhello.dir/build

src/CMakeFiles/skxhello.dir/clean:
	cd /home/shikaixun/test/skx/cmake_learn/cmake/t2/build/src && $(CMAKE_COMMAND) -P CMakeFiles/skxhello.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/skxhello.dir/clean

src/CMakeFiles/skxhello.dir/depend:
	cd /home/shikaixun/test/skx/cmake_learn/cmake/t2/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/shikaixun/test/skx/cmake_learn/cmake/t2 /home/shikaixun/test/skx/cmake_learn/cmake/t2/src /home/shikaixun/test/skx/cmake_learn/cmake/t2/build /home/shikaixun/test/skx/cmake_learn/cmake/t2/build/src /home/shikaixun/test/skx/cmake_learn/cmake/t2/build/src/CMakeFiles/skxhello.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/skxhello.dir/depend


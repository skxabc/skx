# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

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
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build

# Include any dependencies generated for this target.
include c/bin/CMakeFiles/C_SKX.dir/depend.make

# Include the progress variables for this target.
include c/bin/CMakeFiles/C_SKX.dir/progress.make

# Include the compile flags for this target's objects.
include c/bin/CMakeFiles/C_SKX.dir/flags.make

c/bin/CMakeFiles/C_SKX.dir/2_dimentional_pointer.o: c/bin/CMakeFiles/C_SKX.dir/flags.make
c/bin/CMakeFiles/C_SKX.dir/2_dimentional_pointer.o: ../c/src/2_dimentional_pointer.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object c/bin/CMakeFiles/C_SKX.dir/2_dimentional_pointer.o"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c/bin && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/C_SKX.dir/2_dimentional_pointer.o   -c /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c/src/2_dimentional_pointer.c

c/bin/CMakeFiles/C_SKX.dir/2_dimentional_pointer.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/C_SKX.dir/2_dimentional_pointer.i"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c/bin && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c/src/2_dimentional_pointer.c > CMakeFiles/C_SKX.dir/2_dimentional_pointer.i

c/bin/CMakeFiles/C_SKX.dir/2_dimentional_pointer.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/C_SKX.dir/2_dimentional_pointer.s"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c/bin && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c/src/2_dimentional_pointer.c -o CMakeFiles/C_SKX.dir/2_dimentional_pointer.s

# Object files for target C_SKX
C_SKX_OBJECTS = \
"CMakeFiles/C_SKX.dir/2_dimentional_pointer.o"

# External object files for target C_SKX
C_SKX_EXTERNAL_OBJECTS =

c/bin/C_SKX: c/bin/CMakeFiles/C_SKX.dir/2_dimentional_pointer.o
c/bin/C_SKX: c/bin/CMakeFiles/C_SKX.dir/build.make
c/bin/C_SKX: c/bin/CMakeFiles/C_SKX.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable C_SKX"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c/bin && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/C_SKX.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
c/bin/CMakeFiles/C_SKX.dir/build: c/bin/C_SKX

.PHONY : c/bin/CMakeFiles/C_SKX.dir/build

c/bin/CMakeFiles/C_SKX.dir/clean:
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c/bin && $(CMAKE_COMMAND) -P CMakeFiles/C_SKX.dir/cmake_clean.cmake
.PHONY : c/bin/CMakeFiles/C_SKX.dir/clean

c/bin/CMakeFiles/C_SKX.dir/depend:
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c/src /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c/bin /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c/bin/CMakeFiles/C_SKX.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : c/bin/CMakeFiles/C_SKX.dir/depend

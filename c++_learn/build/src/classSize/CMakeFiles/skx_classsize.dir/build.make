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
CMAKE_SOURCE_DIR = /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build

# Include any dependencies generated for this target.
include src/classSize/CMakeFiles/skx_classsize.dir/depend.make

# Include the progress variables for this target.
include src/classSize/CMakeFiles/skx_classsize.dir/progress.make

# Include the compile flags for this target's objects.
include src/classSize/CMakeFiles/skx_classsize.dir/flags.make

src/classSize/CMakeFiles/skx_classsize.dir/classsizeof.o: src/classSize/CMakeFiles/skx_classsize.dir/flags.make
src/classSize/CMakeFiles/skx_classsize.dir/classsizeof.o: ../src/classSize/classsizeof.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/classSize/CMakeFiles/skx_classsize.dir/classsizeof.o"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/src/classSize && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/skx_classsize.dir/classsizeof.o -c /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/src/classSize/classsizeof.cpp

src/classSize/CMakeFiles/skx_classsize.dir/classsizeof.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/skx_classsize.dir/classsizeof.i"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/src/classSize && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/src/classSize/classsizeof.cpp > CMakeFiles/skx_classsize.dir/classsizeof.i

src/classSize/CMakeFiles/skx_classsize.dir/classsizeof.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/skx_classsize.dir/classsizeof.s"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/src/classSize && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/src/classSize/classsizeof.cpp -o CMakeFiles/skx_classsize.dir/classsizeof.s

# Object files for target skx_classsize
skx_classsize_OBJECTS = \
"CMakeFiles/skx_classsize.dir/classsizeof.o"

# External object files for target skx_classsize
skx_classsize_EXTERNAL_OBJECTS =

bin/skx_classsize: src/classSize/CMakeFiles/skx_classsize.dir/classsizeof.o
bin/skx_classsize: src/classSize/CMakeFiles/skx_classsize.dir/build.make
bin/skx_classsize: src/classSize/CMakeFiles/skx_classsize.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/skx_classsize"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/src/classSize && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/skx_classsize.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/classSize/CMakeFiles/skx_classsize.dir/build: bin/skx_classsize

.PHONY : src/classSize/CMakeFiles/skx_classsize.dir/build

src/classSize/CMakeFiles/skx_classsize.dir/clean:
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/src/classSize && $(CMAKE_COMMAND) -P CMakeFiles/skx_classsize.dir/cmake_clean.cmake
.PHONY : src/classSize/CMakeFiles/skx_classsize.dir/clean

src/classSize/CMakeFiles/skx_classsize.dir/depend:
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/src/classSize /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/src/classSize /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/build/src/classSize/CMakeFiles/skx_classsize.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/classSize/CMakeFiles/skx_classsize.dir/depend


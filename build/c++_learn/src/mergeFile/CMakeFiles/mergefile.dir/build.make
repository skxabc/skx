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
include c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/depend.make

# Include the progress variables for this target.
include c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/progress.make

# Include the compile flags for this target's objects.
include c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/flags.make

c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/merge_opus_files_2_1.o: c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/flags.make
c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/merge_opus_files_2_1.o: ../c++_learn/src/mergeFile/merge_opus_files_2_1.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/merge_opus_files_2_1.o"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/mergeFile && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/mergefile.dir/merge_opus_files_2_1.o -c /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/src/mergeFile/merge_opus_files_2_1.cpp

c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/merge_opus_files_2_1.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/mergefile.dir/merge_opus_files_2_1.i"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/mergeFile && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/src/mergeFile/merge_opus_files_2_1.cpp > CMakeFiles/mergefile.dir/merge_opus_files_2_1.i

c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/merge_opus_files_2_1.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/mergefile.dir/merge_opus_files_2_1.s"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/mergeFile && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/src/mergeFile/merge_opus_files_2_1.cpp -o CMakeFiles/mergefile.dir/merge_opus_files_2_1.s

# Object files for target mergefile
mergefile_OBJECTS = \
"CMakeFiles/mergefile.dir/merge_opus_files_2_1.o"

# External object files for target mergefile
mergefile_EXTERNAL_OBJECTS =

c++_learn/bin/mergefile: c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/merge_opus_files_2_1.o
c++_learn/bin/mergefile: c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/build.make
c++_learn/bin/mergefile: c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../bin/mergefile"
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/mergeFile && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/mergefile.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/build: c++_learn/bin/mergefile

.PHONY : c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/build

c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/clean:
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/mergeFile && $(CMAKE_COMMAND) -P CMakeFiles/mergefile.dir/cmake_clean.cmake
.PHONY : c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/clean

c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/depend:
	cd /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/c++_learn/src/mergeFile /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/mergeFile /home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skx/build/c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : c++_learn/src/mergeFile/CMakeFiles/mergefile.dir/depend


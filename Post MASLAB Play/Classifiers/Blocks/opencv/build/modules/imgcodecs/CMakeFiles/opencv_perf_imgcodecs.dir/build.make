# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.9

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

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = C:\Users\arinz\Desktop\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Lib\site-packages\cmake\data\bin\cmake.exe

# The command to remove a file.
RM = C:\Users\arinz\Desktop\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Lib\site-packages\cmake\data\bin\cmake.exe -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build

# Include any dependencies generated for this target.
include modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/depend.make

# Include the progress variables for this target.
include modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/progress.make

# Include the compile flags for this target's objects.
include modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/flags.make

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/flags.make
modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/includes_CXX.rsp
modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj: ../modules/imgcodecs/perf/perf_main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj"
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\imgcodecs && C:\Users\arinz\Desktop\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Scripts\g++.exe  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS)  -Winvalid-pch  -include "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/imgcodecs/perf_precomp.hpp" -o CMakeFiles\opencv_perf_imgcodecs.dir\perf\perf_main.cpp.obj -c C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\modules\imgcodecs\perf\perf_main.cpp

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.i"
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\imgcodecs && C:\Users\arinz\Desktop\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Scripts\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS)  -Winvalid-pch  -include "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/imgcodecs/perf_precomp.hpp" -E C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\modules\imgcodecs\perf\perf_main.cpp > CMakeFiles\opencv_perf_imgcodecs.dir\perf\perf_main.cpp.i

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.s"
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\imgcodecs && C:\Users\arinz\Desktop\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Scripts\g++.exe $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS)  -Winvalid-pch  -include "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/imgcodecs/perf_precomp.hpp" -S C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\modules\imgcodecs\perf\perf_main.cpp -o CMakeFiles\opencv_perf_imgcodecs.dir\perf\perf_main.cpp.s

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj.requires:

.PHONY : modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj.requires

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj.provides: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj.requires
	$(MAKE) -f modules\imgcodecs\CMakeFiles\opencv_perf_imgcodecs.dir\build.make modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj.provides.build
.PHONY : modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj.provides

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj.provides.build: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj


# Object files for target opencv_perf_imgcodecs
opencv_perf_imgcodecs_OBJECTS = \
"CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj"

# External object files for target opencv_perf_imgcodecs
opencv_perf_imgcodecs_EXTERNAL_OBJECTS =

bin/opencv_perf_imgcodecs.exe: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj
bin/opencv_perf_imgcodecs.exe: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/build.make
bin/opencv_perf_imgcodecs.exe: lib/libopencv_ts330.a
bin/opencv_perf_imgcodecs.exe: lib/libopencv_highgui330.dll.a
bin/opencv_perf_imgcodecs.exe: lib/libopencv_videoio330.dll.a
bin/opencv_perf_imgcodecs.exe: lib/libopencv_imgcodecs330.dll.a
bin/opencv_perf_imgcodecs.exe: lib/libopencv_imgproc330.dll.a
bin/opencv_perf_imgcodecs.exe: lib/libopencv_core330.dll.a
bin/opencv_perf_imgcodecs.exe: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/linklibs.rsp
bin/opencv_perf_imgcodecs.exe: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/objects1.rsp
bin/opencv_perf_imgcodecs.exe: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ..\..\bin\opencv_perf_imgcodecs.exe"
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\imgcodecs && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\opencv_perf_imgcodecs.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/build: bin/opencv_perf_imgcodecs.exe

.PHONY : modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/build

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/requires: modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/perf/perf_main.cpp.obj.requires

.PHONY : modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/requires

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/clean:
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\imgcodecs && $(CMAKE_COMMAND) -P CMakeFiles\opencv_perf_imgcodecs.dir\cmake_clean.cmake
.PHONY : modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/clean

modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\modules\imgcodecs C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\imgcodecs C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\imgcodecs\CMakeFiles\opencv_perf_imgcodecs.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : modules/imgcodecs/CMakeFiles/opencv_perf_imgcodecs.dir/depend


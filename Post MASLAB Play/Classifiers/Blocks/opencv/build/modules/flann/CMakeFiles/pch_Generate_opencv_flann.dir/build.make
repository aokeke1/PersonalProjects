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

# Utility rule file for pch_Generate_opencv_flann.

# Include the progress variables for this target.
include modules/flann/CMakeFiles/pch_Generate_opencv_flann.dir/progress.make

modules/flann/CMakeFiles/pch_Generate_opencv_flann: modules/flann/precomp.hpp.gch/opencv_flann_Release.gch


modules/flann/precomp.hpp.gch/opencv_flann_Release.gch: ../modules/flann/src/precomp.hpp
modules/flann/precomp.hpp.gch/opencv_flann_Release.gch: modules/flann/precomp.hpp
modules/flann/precomp.hpp.gch/opencv_flann_Release.gch: lib/libopencv_flann_pch_dephelp.a
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating precomp.hpp.gch/opencv_flann_Release.gch"
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\flann && C:\Users\arinz\Desktop\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Lib\site-packages\cmake\data\bin\cmake.exe -E make_directory C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/flann/precomp.hpp.gch
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\flann && C:\Users\arinz\Desktop\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Scripts\g++.exe -O2 -DNDEBUG -DNDEBUG "-D__OPENCV_BUILD=1" "-D_USE_MATH_DEFINES" "-D__STDC_CONSTANT_MACROS" "-D__STDC_LIMIT_MACROS" "-D__STDC_FORMAT_MACROS" -I"C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build" -I"C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build" -I"C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/flann/include" -I"C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/flann/src" -I"C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/flann" -I"C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/core/include" -fsigned-char -mstackrealign -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Winit-self -Wno-narrowing -Wno-delete-non-virtual-dtor -Wno-comment -fdiagnostics-show-option -Wno-long-long -fomit-frame-pointer -ffunction-sections -msse -msse2 -msse3 -fvisibility=hidden -fvisibility-inlines-hidden -DCVAPI_EXPORTS -x c++-header -o C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/flann/precomp.hpp.gch/opencv_flann_Release.gch C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/flann/precomp.hpp

modules/flann/precomp.hpp: ../modules/flann/src/precomp.hpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Generating precomp.hpp"
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\flann && C:\Users\arinz\Desktop\WinPython-64bit-2.7.10.3\python-2.7.10.amd64\Lib\site-packages\cmake\data\bin\cmake.exe -E copy_if_different C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/flann/src/precomp.hpp C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/flann/precomp.hpp

pch_Generate_opencv_flann: modules/flann/CMakeFiles/pch_Generate_opencv_flann
pch_Generate_opencv_flann: modules/flann/precomp.hpp.gch/opencv_flann_Release.gch
pch_Generate_opencv_flann: modules/flann/precomp.hpp
pch_Generate_opencv_flann: modules/flann/CMakeFiles/pch_Generate_opencv_flann.dir/build.make

.PHONY : pch_Generate_opencv_flann

# Rule to build all files generated by this target.
modules/flann/CMakeFiles/pch_Generate_opencv_flann.dir/build: pch_Generate_opencv_flann

.PHONY : modules/flann/CMakeFiles/pch_Generate_opencv_flann.dir/build

modules/flann/CMakeFiles/pch_Generate_opencv_flann.dir/clean:
	cd /d C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\flann && $(CMAKE_COMMAND) -P CMakeFiles\pch_Generate_opencv_flann.dir\cmake_clean.cmake
.PHONY : modules/flann/CMakeFiles/pch_Generate_opencv_flann.dir/clean

modules/flann/CMakeFiles/pch_Generate_opencv_flann.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\modules\flann C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\flann C:\Users\arinz\Desktop\2016-2017\Projects\Github\PersonalProjects\Post_MASLAB_Play\Classifiers\Blocks\opencv\build\modules\flann\CMakeFiles\pch_Generate_opencv_flann.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : modules/flann/CMakeFiles/pch_Generate_opencv_flann.dir/depend


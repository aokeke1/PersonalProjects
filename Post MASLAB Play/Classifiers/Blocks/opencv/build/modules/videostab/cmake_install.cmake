# Install script for directory: C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/x64/mingw/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/lib/libopencv_videostab330.dll.a")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "libs" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/x64/mingw/bin" TYPE SHARED_LIBRARY OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/bin/libopencv_videostab330.dll")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/x64/mingw/bin/libopencv_videostab330.dll" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/x64/mingw/bin/libopencv_videostab330.dll")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "C:/Users/arinz/Desktop/WinPython-64bit-2.7.10.3/python-2.7.10.amd64/Scripts/strip.exe" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/x64/mingw/bin/libopencv_videostab330.dll")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/deblurring.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/fast_marching.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/fast_marching_inl.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/frame_source.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/global_motion.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/inpainting.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/log.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/motion_core.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/motion_stabilizing.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/optical_flow.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/outlier_rejection.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/ring_buffer.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/stabilizer.hpp")
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "dev" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/opencv2/videostab" TYPE FILE OPTIONAL FILES "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/videostab/include/opencv2/videostab/wobble_suppression.hpp")
endif()


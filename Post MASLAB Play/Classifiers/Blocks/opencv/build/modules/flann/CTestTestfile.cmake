# CMake generated Testfile for 
# Source directory: C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/modules/flann
# Build directory: C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/modules/flann
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_flann "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/bin/opencv_test_flann.exe" "--gtest_output=xml:opencv_test_flann.xml")
set_tests_properties(opencv_test_flann PROPERTIES  LABELS "Main;opencv_flann;Accuracy" WORKING_DIRECTORY "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/test-reports/accuracy")

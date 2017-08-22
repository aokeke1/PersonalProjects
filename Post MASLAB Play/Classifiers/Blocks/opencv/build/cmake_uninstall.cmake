# -----------------------------------------------
# File that provides "make uninstall" target
#  We use the file 'install_manifest.txt'
# -----------------------------------------------
IF(NOT EXISTS "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/install_manifest.txt")
  MESSAGE(FATAL_ERROR "Cannot find install manifest: \"C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/install_manifest.txt\"")
ENDIF(NOT EXISTS "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/install_manifest.txt")

FILE(READ "C:/Users/arinz/Desktop/2016-2017/Projects/Github/PersonalProjects/Post_MASLAB_Play/Classifiers/Blocks/opencv/build/install_manifest.txt" files)
STRING(REGEX REPLACE "\n" ";" files "${files}")
FOREACH(file ${files})
  MESSAGE(STATUS "Uninstalling \"$ENV{DESTDIR}${file}\"")
  IF(EXISTS "$ENV{DESTDIR}${file}")
    EXEC_PROGRAM(
      "C:/Users/arinz/Desktop/WinPython-64bit-2.7.10.3/python-2.7.10.amd64/Lib/site-packages/cmake/data/bin/cmake.exe" ARGS "-E remove \"$ENV{DESTDIR}${file}\""
      OUTPUT_VARIABLE rm_out
      RETURN_VALUE rm_retval
      )
    IF(NOT "${rm_retval}" STREQUAL 0)
      MESSAGE(FATAL_ERROR "Problem when removing \"$ENV{DESTDIR}${file}\"")
    ENDIF(NOT "${rm_retval}" STREQUAL 0)
  ELSE(EXISTS "$ENV{DESTDIR}${file}")
    MESSAGE(STATUS "File \"$ENV{DESTDIR}${file}\" does not exist.")
  ENDIF(EXISTS "$ENV{DESTDIR}${file}")
ENDFOREACH(file)

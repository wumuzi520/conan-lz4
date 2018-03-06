#
# Find LZ4
#
#  LIBLZ4_INCLUDE_DIR - where to find lz4.h, etc.
#  LIBLZ4_LIBRARY     - List of libraries when using liblz4.
#  LIBLZ4_FOUND       - True if liblz4 found.

FIND_PATH(LIBLZ4_INCLUDE_DIR lz4.h)

FIND_LIBRARY(LIBLZ4_LIBRARY NAMES lz4)

# handle the QUIETLY and REQUIRED arguments and set LIBLZ4_FOUND to TRUE if
# all listed variables are TRUE
INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(LZ4 DEFAULT_MSG LIBLZ4_LIBRARY LIBLZ4_INCLUDE_DIR)

MARK_AS_ADVANCED(LIBLZ4_LIBRARY LIBLZ4_INCLUDE_DIR)


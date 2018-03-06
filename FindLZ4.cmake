#
# Find LZ4
#
#  LZ4_INCLUDE_DIR - where to find lz4.h, etc.
#  LZ4_LIBRARY     - List of libraries when using liblz4.
#  LZ4_FOUND       - True if liblz4 found.

FIND_PATH(LZ4_INCLUDE_DIR lz4.h)

FIND_LIBRARY(LZ4_LIBRARY NAMES lz4)

# handle the QUIETLY and REQUIRED arguments and set LZ4_FOUND to TRUE if
# all listed variables are TRUE
INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(LZ4 DEFAULT_MSG LZ4_LIBRARY LZ4_INCLUDE_DIR)

MARK_AS_ADVANCED(LZ4_LIBRARY LZ4_INCLUDE_DIR)


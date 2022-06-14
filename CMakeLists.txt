cmake_minimum_required(VERSION 3.14)

#project name と使用言語
project(pyJaids CXX)
set(PYJAIDS_VERSION 0.0.1)
cmake_policy(GET CMP0091 New)

# leak check
#add_compile_definitions(CHECK_LEAKED_MEMORY)

##################################################################################
# Version
##################################################################################
set(CMAKE_BUILD_DIR "${CMAKE_BINARY_DIR}")
configure_file (
 "${PROJECT_SOURCE_DIR}/src/JaidsConfig.h.in"
 "${CMAKE_BUILD_DIR}/JaidsConfig_base.h"
 )

# ---------------------------------------------------------------------------------------
# CMAKE_SOURCE_TOP_DIR : refer to the deps
# ---------------------------------------------------------------------------------------
set(CMAKE_SOURCE_TOP_DIR ${CMAKE_SOURCE_DIR})

# ---------------------------------------------------------------------------------------
# Set PYJAIDS_MASTER_PROJECT to ON if we are building pyJaids
# ---------------------------------------------------------------------------------------
if(NOT DEFINED PYJAIDS_MASTER_PROJECT)
    if(CMAKE_PROJECT_NAME STREQUAL pyJaids)
        set(PYJAIDS_MASTER_PROJECT ON)
    else()
        set(PYJAIDS_MASTER_PROJECT OFF)
    endif()
endif()

if(PYJAIDS_MASTER_PROJECT)
    message("////////// PYJAIDS_MASTER_PROJECT //////////:${PYJAIDS_MASTER_PROJECT}")
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    add_subdirectory( src )
    add_subdirectory( test )
endif()



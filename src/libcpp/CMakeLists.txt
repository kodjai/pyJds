set(TARGET_NAME libcpp)
set(CMAKE_DEBUG_POSTFIX _d)

##################################################################################
# target
##################################################################################
add_library(${TARGET_NAME} STATIC)
target_compile_features(${TARGET_NAME} PUBLIC cxx_std_17)
target_include_directories(${TARGET_NAME} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
)

add_library(pyjaids::libcpp ALIAS ${TARGET_NAME})
target_sources(${TARGET_NAME}
  PRIVATE
        mod_buffer.cpp
        mod_buffer.hpp
        mod_device.cpp
        mod_device.hpp
        mod_device_gev.cpp
        mod_device_gev.hpp
        mod_device_u3v.cpp
        mod_device_u3v.hpp
        mod_device_finder.cpp
        mod_device_finder.hpp
        mod_device_info.cpp
        mod_device_info.hpp
        mod_exception.hpp
        mod_host_info.cpp
        mod_host_info.hpp
        mod_image.cpp
        mod_image.hpp
        mod_stream.cpp
        mod_stream.hpp
        mod_stream_gev.cpp
        mod_stream_gev.hpp
        mod_stream_u3v.cpp
        mod_stream_u3v.hpp
        util_converter.cpp
        util_converter.hpp
)

 target_link_libraries(${TARGET_NAME} PRIVATE
     jaids::libstatic
     jaids::util
     jaids::libcommon
)

##################################################################################
# 3rd-party OSS library
##################################################################################

##################################################################################
# Compile Option
##################################################################################
if(UNIX)
find_package(Threads REQUIRED)
set_property(TARGET ${TARGET_NAME} PROPERTY POSITION_INDEPENDENT_CODE ON)
target_link_libraries(${TARGET_NAME} PRIVATE Threads::Threads)
endif()

##################################################################################
# eBUS SDK
##################################################################################
target_include_directories(${TARGET_NAME} PRIVATE $ENV{PUREGEV_ROOT}/Includes)

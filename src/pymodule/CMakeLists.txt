# target name
set(TARGET_NAME "_module")
#set(CMAKE_DEBUG_POSTFIX _d)

cmake_policy(SET CMP0091 NEW)

pybind11_add_module(${TARGET_NAME}
    module.cpp
    module_search_device.cpp
    module_feature.cpp
    )

target_link_libraries(${TARGET_NAME} PRIVATE 
    pyjaids::libcpp
    jaids::libstatic
    jaids::util   
    jaids::libcommon
    )
target_compile_features(${TARGET_NAME} PUBLIC cxx_std_17)



##################################################################################
#output folder
##################################################################################
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")   #dllファイル生成場所

##################################################################################
# Visual Studio Option
##################################################################################
if(MSVC)
# 次の行を追加するとMinSizeRelとRelWithDebInfoの選択肢を生成することが抑制
SET(CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "limited configs" FORCE)
endif()


##################################################################################
# eBUS SDK
##################################################################################
target_link_directories(${TARGET_NAME} PRIVATE $ENV{PUREGEV_ROOT}/Libraries)
#target_include_directories(${TARGET_NAME} PRIVATE $ENV{PUREGEV_ROOT}/Includes)

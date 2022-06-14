
set(TARGET_NAME "ut_mod_image")
# C++17利用
set(CMAKE_CXX_STANDARD 17)
cmake_policy(SET CMP0091 NEW)

##################################################################################
# target
##################################################################################
add_executable(${TARGET_NAME})
target_sources(${TARGET_NAME}
  PRIVATE
	testmain.cpp
    test_ut_converter.cpp
)

target_link_libraries(${TARGET_NAME} PRIVATE
    pyjaids::libcpp
	gtest_main
    jaids::util
    jaids::libstatic
#    C:/Users/nma/AppData/Local/Programs/Python/Python38/libs/python38.lib
)

# except public inteface
target_include_directories(${TARGET_NAME} PRIVATE
    ${PROJECT_SOURCE_DIR}/src
)

if(MSVC)
  set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
  set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
endif()

##################################################################################
# 3rd-party OSS library
##################################################################################


##################################################################################
# eBUS SDK
##################################################################################
if(MSVC)
target_link_directories(${TARGET_NAME} PRIVATE $ENV{PUREGEV_ROOT}/Libraries)
else()
target_link_directories(${TARGET_NAME} PRIVATE $ENV{PUREGEV_ROOT}/lib)
endif()

include(GoogleTest)
#add_test(NAME run_test COMMAND ${TARGET_NAME})
#gtest_add_tests(TARGET ${TARGET_NAME})
gtest_discover_tests(${TARGET_NAME})